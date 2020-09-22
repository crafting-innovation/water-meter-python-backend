import requests
import decimal
from json import dumps
pload = {'project':'salarpuria','types':'slab','tax':18,'minimum':100,'cpl_1':0.19,'cpl_2':0.21,'cpl_3':0.23,'cpl_4':0.26,'cpl_5':0.30,
         'slab1_limit':8000000,'slab1_rate':0.1,'slab2_limit':10000000,'slab2_rate':0.12,'slab3_rate':0.45,'slab3_limit':12000000,'slab3_rate':0.15,
         'slab4_limit':15000000,'slab4_rate':0.19,'slab5_rate':0.24}
r = requests.post('https://jwodtc0y96.execute-api.ap-south-1.amazonaws.com/dev/resume?service=put-item-meter-card',data=dumps(pload))
print(r.json())
