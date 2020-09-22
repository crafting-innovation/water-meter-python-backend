import requests
import decimal
from datetime import datetime,timedelta
from json import dumps
pload = {'wing':'W1','flat':'101','project':'salarpuria','subject':'device not working','description':'water device not showing data','timestamp':int(datetime.now().timestamp())}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=raise-ticket',data=dumps(pload))
print(r.json())
