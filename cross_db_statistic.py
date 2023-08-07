import pandas as pd
import itertools
from pathlib import Path


# Combining and deduplicating all species in territory-oriented lists into one 
species_list = set(itertools.chain(*[ species.read_text().split('\n') for species in Path('./species').iterdir()]))
output = {}

def get_gb_count(species: str):
    file = Path(f'./data/genbank/{species}.gb')
    if file.exists():
        return file.read_text().count('//')
    return 0

def get_bold_count(species):
    file = Path(f'./data/bold/{species}.tsv')
    if file.exists():
        df = pd.read_csv(file, sep='\t', encoding='cp1252')
        df = df.fillna('')
        df = df[df.species_name.str.lower()==species.lower()]
        # Only markercodes with 'COI-' or empty will be accounted
        df = df[(df.markercode.str.contains('COI-')) | (df.markercode.str.strip()=='')]
        return len(set(df.processid))   
    else: return 0


for species in species_list:
    output[species]={}
    output[species]['gb'] = get_gb_count(species) 
    output[species]['bold'] = get_bold_count(species)

species = pd.DataFrame.from_dict(output, orient ='index')
species = species.reset_index()
species.columns = ['species', 'gb','bold']
species.to_csv(f'cross_db_species_count.tsv',sep='\t', index=False)