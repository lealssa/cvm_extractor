import json
from datetime import datetime, date
from dateutil.rrule import rrule, MONTHLY

def get_config():
    '''
    Retorna um dict com o as configs do arquivo config.json
    '''    
    config_file = './config.json'
    config = {}

    with open(config_file,'r') as f:
        config = json.loads(f.read())

    return config

config = get_config()

def parse_values(input_dict):
    '''
    Converte valores de um dicionario para os tipos do MongoDB
    '''
    for k,v in [(k,v) for (k,v) in input_dict.items()]:        
        try:
            prefix = k[0:3]
            if prefix in config['cvm_float_values_prefix']:
                input_dict[k] = float(v)
                pass

            if prefix in config['cvm_date_values_prefix']:
                input_dict[k] = datetime.strptime(v, "%Y-%m-%d")
                pass              

        except ValueError:
            pass

    return input_dict


def gen_month_list(start_dt):
    '''
    Gera uma lista contendo todos os meses a partir de uma data inicial.
    Ex.: ['202109','202110']
    '''
    end_dt = date.today()

    dates = [dt.strftime('%Y%m') for dt in rrule(MONTHLY, dtstart=start_dt, until=end_dt)]

    return dates
