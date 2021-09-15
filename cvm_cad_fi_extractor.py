import json
from utils import config, parse_values
import requests
import csv
import bson
from pymongo import UpdateOne, MongoClient

# Pega cadastro dos FIs na CVM e insere numa lista
mongodb_bulk_list = []

with requests.Session() as s:

    download = s.get(config['cvm_cad_fi_file'])
    
    if not download.ok:
        raise Exception(download)    

    decoded_content = download.content.decode('latin1')
    reader = csv.DictReader(decoded_content.splitlines(), delimiter=';')
    
    for row in [ r for r in reader if r['SIT'] != 'CANCELADA' ]:
        row = parse_values(row)
        mongodb_bulk_list.append(
            UpdateOne({'CNPJ_FUNDO': row['CNPJ_FUNDO']}, {'$set': row}, upsert=True)
        )

# Cadastra lista no MongoDB via bulk update (atualiza se existir)
with MongoClient(config['cvm_mongodb_url']) as client:
    db = client['cvm_extractor']
    db.cvm_cad_fi.bulk_write(mongodb_bulk_list, ordered=False)
