import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'flat':'W1103','vehicle_no':'KA-05 HD 2338','type':'Car','model':'city','project':'salarpuria','brand':'Honda','rfid':'1234567891011127'}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=insert-rfid-info',data=dumps(pload))
print(r.json())
