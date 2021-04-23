import configparser as ConfigParser  # Python 3

class configFile:
    def __init__(self,**kwargs):
        # import config file could depending on the name of the config file
        if not kwargs.get("configFilename"):
            self.configFilename = 'config.cfg'
        else:
            self.configFilename = kwargs.get("configFilename")

        self.config = ConfigParser.ConfigParser()

        self.read()

    def configuration(self):
        return self.config

    def read(self):
        print(f"reading configuration file : {self.configFilename}")
        self.config.read(self.configFilename)

    def changeConfig(self, section, option, value):
        self.config.set(section, option, value)
        with open(self.configFilename, 'w') as configfile:
            self.config.write(configfile)

    # Functions with Arguments---------------------------------------------------
    # Functions to modify the config.cfg-----------------------------------------
    # This function modify the name of the file in the config.cfg
    def NewFile(self, fileText):
        if not fileText:
            fileText = "Measures_ "
        elif not fileText[-1]=="_":
            fileText += "_"

        self.changeConfig('filenameLogger', 'filename',fileText)


    # This function modify the directory of the file that you want to read
    def NewPath(self, pathText):
        if not pathText:
            pathText = "./save_measures/"
        elif not pathText[-1]=="/":
            pathText += "/"
        
        self.changeConfig('filenameLogger', 'folderpath', pathText)

    # This changes the data interval time the values is between 8ms to 1000ms
    def SetDataInterval(self, dataInterval):
        self.changeConfig('encoder', 'datainterval', str(dataInterval))
