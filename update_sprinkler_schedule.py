import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'hour':10,'area':'sports ground','project':'salarpuria','minutes':40,'duration':30}
r = requests.post('https://emldnitw6f.execute-api.ap-south-1.amazonaws.com/dev/resume?service=update-sprinkler-schedule',data=dumps(pload))
print(r.json())
