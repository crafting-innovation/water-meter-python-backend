import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'access_card_id':'123456789','timestamp':int(datetime.now().timestamp()),'amenity':'gym','project':'salarpuria','type':'OUT'}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=insert-aminity-data',data=dumps(pload))
print(r.json())
