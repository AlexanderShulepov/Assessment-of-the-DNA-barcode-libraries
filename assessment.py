import re
import pandas as pd
from pathlib import Path

GENBANK_DATA = Path('./data/genbank')
BOLD_DATA = Path('./data/bold')
configs = Path('./species/').iterdir()


def check_species_bold(species):
    return (BOLD_DATA / Path(species).with_suffix('.tsv')).exists()


def check_species_genbank(species):
    return (GENBANK_DATA / Path(species).with_suffix('.gb')).exists()


def process_genbank_species(species, filter:bool=False, territory_preset:str=''):
    '''
    Extracting all ids  of sequences from genbank data for species.
    In the case of some territory lists  we interested also in filtering by some country

    species: str - species name and filename of genbank file
    filter: bool - if set True then sequences will be filtered by using territory preset
    territory_preset: str:  is used for searching only sequences in specified countries. 
    If filter set True then required.
        canada_alaska - containing somthing of [canada, alaska] in country
        ne_europe - containing somthing of [n orway, finland, sweden, kareliya ] in country
        russia_ws - returning empty results

    '''
    data = (GENBANK_DATA / Path(species).with_suffix('.gb')).read_text().strip()
    sequences = []
    for sequence in data.split('//'):
        if not sequence:
            continue
        xref = re.findall(r'db_xref="BOLD:(.*)\.', sequence)
        xref = xref[0] if xref else xref
        accession = re.findall(r'ACCESSION\s+(.*)', sequence)
        accession = accession[0] if accession else accession
        if filter:
            country = re.findall(r'/country="(.*)', sequence)
            country = country[0].lower() if country else ''
            if territory_preset=='canada_alaska' and 'alaska' not in country and  'canada' not in country:
                continue
            if territory_preset=='ne_europe' and 'norway' not in country and  'finland' not in country and  'sweden' not in country and  'kareliya' not in country:
                continue
            if territory_preset=='russia_ws':
                continue
        sequences.append(xref if xref else accession)
    return sequences


def process_bold_species(species, filter:bool=False,territory_preset:str=''):
    '''
    Extracting all ids  of sequences from genbank data for species.
    In the case of some territory lists  we interested also in filtering by some country
    Only markercodes with 'COI-' or empty will be accounted
    If sequences is mined from genbank then we need sampleid from that database, in other case we need bold processid 

    species: str - species name and filename of genbank file
    filter: bool - if set True then sequences will be filtered by using territory preset
    territory_preset: str:  is used for searching only sequences in specified countries. 
    If filter set True then required.
        canada_alaska - containing somthing of [canada, alaska] in country
        ne_europe - containing somthing of [n orway, finland, sweden, kareliya ] in country
        russia_ws - returning empty results

    '''
    def computed_id_set (row):
        if row["institution_storing"]=='Mined from GenBank, NCBI':
            return row['sampleid']
        else:
            return row['processid']

    data = (BOLD_DATA / Path(species).with_suffix('.tsv'))
    df = pd.read_csv(data, sep='\t', encoding='cp1252')
    df = df.fillna('')
    if filter:
        if territory_preset=='canada_alaska':
            df = df[(df.country.str.lower()=='canada') | (df.province_state.str.lower()=='alaska')]
        if territory_preset=='ne_europe':   
            df = df[df.country.str.lower().isin(["finland", "norway", "sweden", "kareliya"])]
        if territory_preset=='russia_ws':   
            df = df[0:0]

    df = df[df.species_name.str.lower()==species.lower()]
    df = df[(df.markercode.str.contains('COI-')) | (df.markercode.str.strip()=='')]
    df["computed_id"] =  df.apply (lambda row: computed_id_set(row), axis=1)
    return list(df["computed_id"])



if __name__=='main':
    # preloaded correct mapping for species - family for all sequences  of interest
    species_family = pd.read_csv('./species_subfamily_mapping.csv',sep=';',encoding='cp1252',names=['species', 'subfamily'], header=0)

    # result of previous step - cross db count of species for all terriorries
    species_total_count = pd.read_csv('./cross_db_species_count.tsv',sep='\t', encoding='cp1252')
    
    for config in configs:
        
        list_name = config.name
        list_data = config.read_text().split('\n')
        output = {}
        for species in list_data:

            if  output.get(species):
                continue
            else:
                output[species]={}
            bold_sequences = []
            genbank_sequences = []
            genbank_sequences_by_country=[]
            bold_sequences_by_country=[]

            if check_species_genbank(species):
                genbank_sequences = process_genbank_species(species)
                genbank_sequences_by_country = process_genbank_species(species, filter=True, territory_preset=list_name)
            
            if check_species_bold(species):
                bold_sequences = process_bold_species(species)
                bold_sequences_by_country = process_bold_species(species,filter=True, territory_preset=list_name)
            
            unique = set(bold_sequences + genbank_sequences)
            intersection = set(bold_sequences).intersection(set(genbank_sequences))
            unique_by_country = set(bold_sequences_by_country + genbank_sequences_by_country)
            
            output[species] = dict(
                intersection=len(intersection),
                unique=len(unique),
                unique_by_country=len(unique_by_country),
                genbank_by_country=len(genbank_sequences_by_country),
                bold_by_country=len(bold_sequences_by_country)
                )

        
        species = pd.DataFrame.from_dict(output, orient ='index')
        species = species.reset_index()
        species.columns = ['species', 'intersection', 'unique', 'unique_by_country', 'genbank_by_country', 'bold_by_country'] 
        subfamily_step = pd.merge(species, species_family, on="species", how='left')
        pd.merge(subfamily_step, species_total_count, on="species", how='left').to_csv(f'result/{list_name}.tsv',sep='\t', index=False)
