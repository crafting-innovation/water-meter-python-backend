import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'project':'salarpuria','service1':'gym','number':"3",'service2':'spa','service3':'club house'}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=insert-aminity-list',data=dumps(pload))
print(r.json())
