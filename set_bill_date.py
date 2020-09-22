import requests
import decimal
from datetime import datetime
from json import dumps
pload = {'project':'salarpuria','day':28,'address':'#1078 Salarpuria XYZ 14th main 6th cross HSR layout somsundarpalya bengaluru - 580800'}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=set-billing-date',data=dumps(pload))
print(r.json())
