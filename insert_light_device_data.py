import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'light_id':'7002L','area':'block-1','project':'salarpuria','status':0,'number':15,'start_hour':18,'start_minutes':0,'duration_hour':12,'duration_minute':30}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=put-lighting-data',data=dumps(pload))
print(r.json())
