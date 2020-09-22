import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'device_id':'6002B','project':'salarpuria','timestamp':int(datetime.now().timestamp()),'consumption':32656}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=water-meter',data=dumps(pload))
print(r.json())
