import requests
from time import sleep
from pathlib import Path
from assessment import check_species_bold


cookies = {
    'session': '85a2b7tfqjoggoqib11m1ihmc2',
    'https': 'off',
    '_ga': 'GA1.2.1175703654.1678294227',
    '_gid': 'GA1.2.392823234.1678294227',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'session=85a2b7tfqjoggoqib11m1ihmc2; https=off; _ga=GA1.2.1175703654.1678294227; _gid=GA1.2.392823234.1678294227',
    'Origin': 'http://boldsystems.org',
    'Referer': 'http://boldsystems.org/index.php/Public_SearchTerms',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}


def fetch_species(species:str):
    data = f'searchfield="{species}"&downloadtype=tsv%3Afull&reporttype=&id_type=processid&cartToken=general_C2D4A130-95BB-4C8C-8AD3-6C4EE5D595D1'

    response = requests.post(
    'http://boldsystems.org/index.php/Public_DownloadData',
    cookies=cookies,
    headers=headers,
    data=data,
    verify=False,
    )
    return response.content


def save_species(fetch_response:str, species:str):
    if fetch_response:
        with open(Path(f'./data/bold/{species}.tsv'), 'wb') as f:
            f.write(fetch_response)

if __name__=='main':
    configs = Path('./species/').iterdir()
    for config in configs:
        
        list_name = config.name
        list_species = config.read_text().split('\n')

        for species in list_species:

            if check_species_bold(species):
                continue
            else:
                print(f'Download: {species}')
                response = fetch_species(species)
                if response:
                    save_species(
                        fetch_response=response
                        , species=species
                    )
                else:
                    print('No data in Bold')
                    sleep(0.2)