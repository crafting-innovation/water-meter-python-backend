import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'hour':22,'area':'block-1','project':'salarpuria','minutes':30,'duration_hour':7,'duration_minute':30}
r = requests.post('https://emldnitw6f.execute-api.ap-south-1.amazonaws.com/dev/resume?service=update-lighting-schedule',data=dumps(pload))
print(r.json())

