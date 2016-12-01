import re

CONFIG_FILE = '.jbrowse_configuration'


def read_configuration_file(setting):
    config_file = open(CONFIG_FILE, 'r')
    contents = config_file.read()
    temp = re.search(__retrieve_settings()[setting], contents).group(0)
    return re.search('= (.*)\n', temp).group(0)[1:].strip()


def write_configuration_file(setting, contents):
    with open(CONFIG_FILE, 'r') as config_file:
        config_contents = config_file.readlines()
    config_settings = __write_settings()[setting]
    config_contents[config_settings[0]] = config_settings[1] + contents + ' \n'
    with open(CONFIG_FILE, 'w') as config_file:
        config_file.writelines(config_contents)


def __retrieve_settings():
    return {"JBrowse_Root": 'JBrowse Root = (.*)\n',
            "Assembler": 'Assembler = (.*)\n'}


def __write_settings():
    return {"JBrowse_Root": (0, 'JBrowse Root = '),
            "Assembler": (1, 'Assembler = ')}
