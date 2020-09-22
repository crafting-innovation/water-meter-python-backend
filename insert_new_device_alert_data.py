import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'project':'salarpuria','device_id':'6002B','consumption':0,'threshold':0,'timestamp':int(datetime(2020,6,3,13,28,54).timestamp()),'area':'W1101'}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=insert-device-alert-data',data=dumps(pload))
print(r.json())
