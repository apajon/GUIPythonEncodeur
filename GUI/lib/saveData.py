import threading

from api_phidget_n_MQTT.src.lib_global_python import createLoggerFile
from api_phidget_n_MQTT.src.lib_global_python import loggerHandler
from api_phidget_n_MQTT.src.lib_global_python import repeatedTimer

class saveData:
    def __init__(self):
        self.last_t1=0
        pass

    def initFile(self,config):
        self.fh = createLoggerFile.createLoggerFile(config)

    def saveDataMQTT(self, client, config, isChecked):
        if isChecked:
            self.fh = self.initFile(config)
            client.fh = self.fh
            client.printLog = config.getboolean('Logger', 'printLog')
            client.firstLine = config.get('filenameLogger', 'firstLine')
            client.saveLog = config.getboolean('Logger', 'saveLog')

            client.on_message = loggerHandler.on_message
            client.loop_start()

            # topic_encoder = config.get('MQTT', 'topic')
            topic_encoder = config.get('encoder', 'topic_subscribe')
            client.subscribe(topic_encoder)
            return 100
        else:
            client.loop_stop()
            client.fh.close()
            return 0    

    def saveData(self, encoder, config, isChecked):
        if isChecked:
            self.initFile(config)
            self.printLog = config.getboolean('Logger', 'printLog')
            self.firstLine = config.get('filenameLogger', 'firstLine')
            self.saveLog = config.getboolean('Logger', 'saveLog')

            self.threadOnMessage = threading.Thread(target=self.onMessage, args=(self, encoder,))
            self.last_t1=encoder.t1
            self.threadLoop=repeatedTimer.RepeatedTimer(0.001, self.loopCheckMessage, encoder)
            self.threadLoop.start()
            
            # ui.RecordingEnco.setValue(100)
            return 100
        else:
            self.threadLoop.stop()
            self.fh.close()

            # ui.RecordingEnco.setValue(0)
            return 0   

    def saveDataSimple(self,config, isChecked):
        if isChecked:
            self.fh = createLoggerFile.createLoggerFile(config)
            self.printLog = config.getboolean('Logger', 'printLog')
            self.firstLine = config.get('filenameLogger', 'firstLine')
            self.saveLog = config.getboolean('Logger', 'saveLog')

            return 100
        else:
            self.fh.close()
            return 0

    def onMessage(self,encoder):
        firstLine=self.firstLine.split(', ')
        # Print the datas in the terminal
        if self.printLog:
            print(firstLine[0]+" : "+str(encoder.t1))
            print(firstLine[1]+" : "+str(encoder.positionChange))
            print(firstLine[2]+" : "+str(encoder.timeChange))
            print(firstLine[3]+" : "+str(encoder.indexTriggered))
            print("----------")

        # Save the datas in a log file 'fh'
        if self.saveLog:
            self.fh.write(str(encoder.t1)+ ", ")
            self.fh.write(str(encoder.positionChange)+ ", ")
            self.fh.write(str(encoder.timeChange)+ ", ")
            self.fh.write(str(encoder.indexTriggered)+ "\n")

    def loopCheckMessage(self,encoder):
        if encoder.t1 != self.last_t1:
            self.threadOnMessage.start()
