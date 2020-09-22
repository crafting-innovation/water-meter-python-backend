import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'sprinkler_id':'6001S','consumption':100,'project':'salarpuria','timestamp':int(datetime.now().timestamp())}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=sprinklers',data=dumps(pload))
print(r.json())
