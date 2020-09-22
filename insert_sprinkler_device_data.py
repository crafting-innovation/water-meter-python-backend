import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'sprinkler_id':'6001S','area':'lawn','project':'salarpuria','status':0,'number':15,'start_hour':9,'start_minutes':45,'duration':15}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=put-sprinkler-data',data=dumps(pload))
print(r.json())
