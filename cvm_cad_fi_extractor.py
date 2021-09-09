import json
from utils import get_config, dict_values_to_float
import requests
import csv
import bson
from pymongo import UpdateOne, MongoClient

config = get_config()

# Pega cadastro dos FIs na CVM e insere numa lista
mongodb_bulk_list = []

with requests.Session() as s:

    download = s.get(config['cvm_cad_fi_file'])

    decoded_content = download.content.decode('latin1')
    reader = csv.DictReader(decoded_content.splitlines(), delimiter=';')
    
    for row in [ r for r in reader if r['SIT'] != 'CANCELADA' ]:
        #row['_id'] = bson.ObjectId()
        row = dict_values_to_float(row, config['cvm_float_values'])
        mongodb_bulk_list.append(
            UpdateOne({'CNPJ_FUNDO': row['CNPJ_FUNDO']}, {'$set': row}, upsert=True)
        )

# Cadastra lista no MongoDB via bulk update (atualiza se existir)
with MongoClient(config['cvm_mongodb_url']) as client:
    db = client['cvm_extractor']
    db.cvm_cad_fi.bulk_write(mongodb_bulk_list)
