import time
import json
import numpy as np
from api_phidget_n_MQTT.src.lib_global_python import MQTT_client
try:
    import ConfigParser #Python 2
except ImportError:
    import configparser as ConfigParser #Python 3

import os
# Make sure current path is this file path
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

config = ConfigParser.ConfigParser()
config.read('config.cfg')
client = MQTT_client.createClient("Encoder", config)
dataFromFile = np.genfromtxt("Logger_encoder_gel_1cm_v1_00.txt", delimiter=",", names=True)
clientTopic = config.get('MQTT', 'topic')
#print(data)
t1=dataFromFile["TimeRecording"]
positionChange=dataFromFile["PositionChange"]
timeChange=dataFromFile["TimeChange"]
indexTriggered=dataFromFile["IndexTriggered"]
      
for i in range(0, len(dataFromFile["TimeRecording"]),1):
    data=  {
    "TimeRecording": t1[i],
    "PositionChange": positionChange[i],
    "TimeChange": timeChange[i],
    "IndexTriggered": indexTriggered[i]
    }
    json_string = json.dumps(data)
    client.publish(clientTopic,json.dumps(data))
    print(data)
    time.sleep(1)


