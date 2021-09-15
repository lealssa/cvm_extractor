import json

from pymongo.operations import InsertOne
from utils import config, parse_values, gen_month_list
import requests
import csv
import bson
from pymongo import InsertOne,UpdateOne, MongoClient
from datetime import datetime

# Monta a lista de meses para extrair
start_dt = datetime.strptime(config['cvm_inf_diario_fi_init_date'],'%Y-%m-%d').date()
month_list = gen_month_list(start_dt)
month_list.sort()

url_base = config['cvm_inf_diario_fi_url_base']
file_prefix = config['cvm_inf_diario_fi_prefix']

for month in month_list:

    # Pega cadastro dos FIs na CVM e insere numa lista
    mongodb_bulk_list = []    

    init_date = month

    fi_diario_file = f"{url_base}{file_prefix}{init_date}.csv"

    print(fi_diario_file)

    with requests.Session() as s:

        download = s.get(fi_diario_file)

        if not download.ok:
            raise Exception(download)

        decoded_content = download.content.decode('latin1')
        reader = csv.DictReader(decoded_content.splitlines(), delimiter=';')
        
        for row in reader:
            row = parse_values(row)
            mongodb_bulk_list.append(            
                UpdateOne({ '$and': [ {'CNPJ_FUNDO': row['CNPJ_FUNDO']},{'DT_COMPTC': row['DT_COMPTC']} ] }, {'$set': row}, upsert=True)
            )

    # Cadastra lista no MongoDB via bulk update (atualiza se existir)
    with MongoClient(config['cvm_mongodb_url']) as client:
        db = client['cvm_extractor']
        db.cvm_fi_diario.bulk_write(mongodb_bulk_list, ordered=False)
