import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("solin")  # Subscribe to the topic “digitest/test1”, receive any messages published on it


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg

client = mqtt.Client("digi_mqtt_test")  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message
client.username_pw_set('testbroker', password='testbroker@123')
client.tls_set()
client.connect('b-9727a950-b5c4-453f-a30a-31729f224886-1.mq.ap-south-1.amazonaws.com', 8883)
client.loop_forever()

'''client.connect(broker,port)
client.loop_start()
time.sleep(4)
client.loop_stop()
client.disconnect()'''

