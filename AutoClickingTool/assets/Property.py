import configobj


class Property:

    def __init__(self):
        self.__config = configobj.ConfigObj("../assets/conf.ini")

    def get_property(self, prop_name: str):
        return self.__config.get(prop_name)

    def set_property(self, keyword: str, value):
        self.__config[keyword] = value
        self.__config.write()
