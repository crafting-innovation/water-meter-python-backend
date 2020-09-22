import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'rfid':'1234567891011126','type':'IN','timestamp':int(datetime.now().timestamp()),'project':'salarpuria'}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=insert-rfid-data',data=dumps(pload))
print(r.json())
