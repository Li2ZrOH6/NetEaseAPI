import requests,json
from loguru import logger

class NetEaseAPI():
    def __init__(self) -> None:
        with open("config.json") as fp:
            inform = json.load(fp)
        self.address = inform['server_address']
        if inform['login_id'] != "":
            self.login_id, self.password = inform['login_id'],inform['password']
        else:
            self.login_id, self.password = "", ""
        logger.info("Init Success.")
    
    def login(self, password : str = None, login_id : str = None):
        return