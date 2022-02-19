from collections import defaultdict
from enums import class_enumerators
from api import API
import utils
import pprint

_sum = defaultdict(float)
def _add(x):
    _sum['cost'] += float(x)
    return None

# API key and secret location
key_loc = utils.PathConstructor(class_enumerators.PathNames.KEYS_FOLDER.value, class_enumerators.PathNames.KEY.value)._str_path()

# Initialize API client
api_object = API()

# Read Kraken API key and secret stored in local file
api_object.load_key(key_loc)

# prepare request
req_data = {'trades': 'true'}

# query servers
trades_history = api_object.query_private('TradesHistory', req_data)

# process queried data
trades = trades_history['result']['trades']
trades_eur = {key:val for key,val in trades.items() if 'EUR' in val['pair'] and 'USDT' not in val['pair']}
# pprint.pprint(resp_eur)

[_add(val['cost']) for val in trades_eur.values()]
print(_sum.values())