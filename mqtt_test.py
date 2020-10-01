import paho.mqtt.client as mqtt
import time
# AMAZON AWS BROKER URL ADDRESS
broker="b-9727a950-b5c4-453f-a30a-31729f224886-1.mq.ap-south-1.amazonaws.com"
# INBOUND PORT ON WHICH MQTT IS CONFIGURED
port=8883
# LOG CALLBACK
def on_log(client,userdata,level,buf):
    print("log: "+buf)
# FIRED WHEN CONNECTION IS COMPLTETE/DONE
def on_connect(cliebt,userdata,flags,rc):
    if rc==0:
        print("OK CONNECTED")
        ret = client.publish("solin","0")
        
    else:
        print("BAD CONNECTION CODE=",rc)
# CAKKBACK AFTER client.publish IS CALLED INSIDE on_connect()
def on_publish(client,userdata,result):     
    print("data published \n")
    pass
# Instantiating a client object
client = mqtt.Client("python1")
# Binding the on_connect callback function
client.on_connect = on_connect
# Binding the log calllback function
client.on_log = on_log
# Binding the publish callback function
client.on_publish = on_publish 
print("Connecting to broker ",broker)
# Setting the username and password of broker to connect 
client.username_pw_set('testbroker', password='testbroker@123')
# Enable SSL connection 
client.tls_set()
# Connect with the broker
client.connect(broker,port)
client.loop_start()
time.sleep(4)
client.loop_stop()
client.disconnect()

