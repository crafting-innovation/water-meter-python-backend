import requests
import decimal
from json import dumps
pload = {"wing":"W1","flat":"101","area":"bathroom1","status":1}
r = requests.post('https://emldnitw6f.execute-api.ap-south-1.amazonaws.com/dev/resume?service=valve-control',data=dumps(pload))
print(r.json())
# endpoint = control-all-valve for all devices status update and remove area from payload
