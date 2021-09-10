import json

from pymongo.operations import InsertOne
from utils import get_config, dict_values_to_float
import requests
import csv
import bson
from pymongo import InsertOne,UpdateOne, MongoClient

config = get_config()

# Pega cadastro dos FIs na CVM e insere numa lista
mongodb_bulk_list = []

url_base = config['cvm_inf_diario_fi_url_base']
file_prefix = config['cvm_inf_diario_fi_prefix']
init_date = config['cvm_inf_diario_fi_init_date']

fi_diario_file = f"{url_base}{file_prefix}{init_date}.csv"

print(fi_diario_file)

with requests.Session() as s:

    download = s.get(fi_diario_file)

    if not download.ok:
        raise Exception(download)

    decoded_content = download.content.decode('latin1')
    reader = csv.DictReader(decoded_content.splitlines(), delimiter=';')
    
    for row in reader:
        #row['_id'] = bson.ObjectId()
        row = dict_values_to_float(row, config['cvm_float_values'])
        mongodb_bulk_list.append(            
            UpdateOne({ '$and': [ {'CNPJ_FUNDO': row['CNPJ_FUNDO']},{'DT_COMPTC': row['DT_COMPTC']} ] }, {'$set': row}, upsert=True)
        )

# Cadastra lista no MongoDB via bulk update (atualiza se existir)
with MongoClient(config['cvm_mongodb_url']) as client:
    db = client['cvm_extractor']
    db.cvm_fi_diario.bulk_write(mongodb_bulk_list, ordered=False)
