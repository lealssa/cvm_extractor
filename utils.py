import json
from datetime import datetime, date
#import datetime
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

def dict_values_to_float(input_dict,values_to_float):
    ''' 
    Converte os valores de um dict para float de acordo com os
    valores passados
    '''
    for k,v in [(k,v) for (k,v) in input_dict.items() if k in values_to_float]:        
        try:            
            input_dict[k] = float(v)
        except ValueError:
            pass

    return input_dict

def dict_values_to_date(input_dict,values_to_date):
    ''' 
    Converte os valores de um dict para date de acordo com os
    valores passados
    '''
    for k,v in [(k,v) for (k,v) in input_dict.items() if k in values_to_date]:        
        try:            
            input_dict[k] = datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            pass

    return input_dict

def gen_month_list(start_dt):

    end_dt = date.today()

    dates = [dt.strftime('%Y%m') for dt in rrule(MONTHLY, dtstart=start_dt, until=end_dt)]

    return dates
