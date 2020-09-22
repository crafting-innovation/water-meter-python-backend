import requests
import decimal
from json import dumps
pload = {'project':'salarpuria','enable_slab':'no','tax':18.5,'minimum':100,
         'slab_1_limit':8000000,'rate1':0.19,'slab_2_limit':10000000,'rate2':0.21,'rate3':0.23,'slab_3_limit':12000000,'slab_4_limit':15000000,'rate4':0.26,'rate5':0.30}
r = requests.post('https://emldnitw6f.execute-api.ap-south-1.amazonaws.com/dev/resume?service=update-meter',data=dumps(pload))
print(r.json())
