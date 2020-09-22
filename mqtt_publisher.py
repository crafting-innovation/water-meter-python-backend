import paho.mqtt.client as paho
from json import dumps
from datetime import datetime
broker="localhost"
port=1883
def on_publish(client,userdata,result):     
    print("data published \n")
    pass
client1= paho.Client("solin")                   
client1.on_publish = on_publish                          
# connection with the mqtt broker address
client1.connect('mqtt.eclipse.org')
results = {'message':200,'device_id':'6001K','consumption':4554,'timestamp':int(datetime.now().timestamp())}
ret= client1.publish("solin",dumps(results))
