import time
import json
import pandas as pd
import numpy as np
import configparser as ConfigParser  # Python 3
from lib_global_python import MQTT_client

config = ConfigParser.ConfigParser()
config.read('config.cfg')
client = MQTT_client.createClient("Encoder", config)
dataFromFile = np.genfromtxt("Logger_encoder_gel_1cm_v1_00.txt", delimiter=",", names=True)
clientTopic = config.get('MQTT', 'topic_publish')
#print(data)
print(dataFromFile["PositionChange"])
poitionChange=dataFromFile["PositionChange"]
data = {
    "TimeRecording": t1,
    "PositionChange": positionChange,
    "TimeChange": timeChange,
    "IndexTriggered": indexTriggered
}
json_string = json.dumps(data)

#publish 'data' in topic as a JSON string
client.publish(clientTopic,json.dumps(data))