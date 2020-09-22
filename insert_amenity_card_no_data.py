import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'flat':'W1101','access_card_id':'123456789','project':'salarpuria'}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=insert-aminity-flat-mapping',data=dumps(pload))
print(r.json())
