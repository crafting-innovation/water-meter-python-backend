import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'wing':'W3','flat':'105','project':'salarpuria','kitchen':'6046K','bath1':'6047B','bath2':'6048B','bath3':'6049B','misc':'6050M','limit':6400}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=put-item-user_valve',data=dumps(pload))
print(r.json())
