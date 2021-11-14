import configparser
import os
import logging

''' 
method_dxdoiorg                         It sets which method is used by the library pdf2doi when querying dx.doi.org to retrieve the bibtex info
                                        Two possible values are 'text/bibliography; style=bibtex' , 'application/x-bibtex' and
                                        'application/citeproc+json'                             
'''


class config():
    __params={'verbose'   :   True,
            'separator' : os.path.sep,
            'method_dxdoiorg' : 'application/citeproc+json',
            }
    __setters = __params.keys()


    @staticmethod
    def update_params(new_params):
        config.__params.update(new_params)

    @staticmethod
    def get(name):
        return config.__params[name]

    @staticmethod
    def set(name, value):
        if name in config.__setters:
             config.__params[name] = value
        else:
            raise NameError("Name not accepted in set() method")
        #Here we define additional actions to perform when specific parameters are modified
        if name == 'verbose':
            # We change the logger verbosity
            if value: loglevel = logging.INFO
            else: loglevel = logging.CRITICAL
            logger = logging.getLogger("pdf2bib")
            logger.setLevel(level=loglevel)

    @staticmethod
    def ReadParamsINIfile():
        '''
        Reads the parameters stored in the file settings.ini, and stores them in the dict self.params
        If the .ini file does not exist, it creates it with the default values.
        '''
        path_current_directory = os.path.dirname(__file__)
        path_config_file = os.path.join(path_current_directory, 'settings.ini')
        if not(os.path.exists(path_config_file)):
            config.WriteParamsINIfile()
        else:
            config_object = configparser.ConfigParser()
            config_object.optionxform = str
            config_object.read(path_config_file)
            config.__params.update(dict(config_object['DEFAULT']))
            config.ConvertParamsToNumb()

    @staticmethod
    def ConvertParamsToNumb():
        for key,val in config.__params.items():
            if isinstance(val, str) and val.isdigit():
                config.__params[key]=int(val)
    @staticmethod
    def print():
        '''
        Prints all settings
        '''
        for key,val in config.__params.items():
            print(key + " : " + str(val))

    @staticmethod
    def WriteParamsINIfile():
        '''
        Writes the parameters currently stored in in the dict self.params into the file settings.ini
        '''
        #params_dict = {key: str(value) for key, value in (config.__params).items()} #Make sure that each value of the dict is converted to a string
        path_current_directory = os.path.dirname(__file__)
        path_config_file = os.path.join(path_current_directory, 'settings.ini')
        config_object = configparser.ConfigParser()
        config_object.optionxform = str
        #print(config_object)
        config_object['DEFAULT'] = config.__params
        with open(path_config_file, 'w') as configfile: #Write them on file
            config_object.write(configfile)


###########################################








