import requests,json,time,requests.utils
from loguru import logger

class NetEaseAPI():
    def __init__(self) -> None:
        '''
        Initialize the API.
        '''
        with open("config.json") as fp:
            inform = json.load(fp)
        self.address = inform['server_address']
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        logger.info("Init Success.")
    
    def login(self, login_type : int = 1 ,password : str = None, id : str = None):
        '''
        Warning: logging in will storage your cookies to the frontend.
        Use various ways to login.
        login_type : Intager to ways to login:
            1: email
            2: cellphone
        password : Your password, default is none.
        id : Your login id, cellphone number or email address.
        
        Return Value:
        1: Login Failed.
        2: id or pwd not correct.
        '''
        if login_type == 1:
            url = self.address + "/login"
            response = requests.get(url=url,params={'email':id,'password':password},headers=self.headers)
        elif login_type == 2:
            url = self.address + '/login/cellphone'
            response = requests.get(url=url,params={'phone':id,'password':password},headers=self.headers)
        else:
            raise ValueError
        if response.status_code == 200:
            # store the cookies for further usage
            now = int(time.time()) % 20
            self.cookie_path = 'temp_login/temp_login_{}.json'.format(str(now))
            with open(self.cookie_path ,'w') as fp:
                cookies = requests.utils.dict_from_cookiejar(response.cookies)
                json.dump(cookies,fp)
            return 0,json.loads(response.content)
        elif response.status_code == 502:
            logger.warning("id or password not correct.")
            return 2
        else:
            logger.warning("Login Failed:" + str(response.status_code))
            return 1

    def login_check(self):
        '''
        check login status by Fetching cookies.
        '''
        try:
            with open(self.cookie_path ,'r') as fp:
                cookies = json.load(fp)
        except AttributeError:
            logger.warning("Warning : Not login")
            cookies = None
        return cookies

    def default_request_get(self,url : str,need_login : bool = False,**kwargs):
        '''
        A universal code for requesting, in order to optimize code structure.
        **kwargs : Optional, dict for params.
        url : requesting url after server address.
        '''
        url = self.address + url
        cookies = self.login_check()
        if cookies != None:
            cookies = requests.utils.cookiejar_from_dict(cookies)
        elif need_login == True:
            return False
        else:
            pass
        response = requests.get(url=url,cookies=cookies,headers=self.headers,params=kwargs)
        if response.status_code == 200:
            resp = json.loads(response.content)
            return resp
        else:
            logger.error("Error: " + str(response.status_code))
            return False
        
    def get_recommend_songs(self):
        '''
        Get your recommand songs.
        '''
        url = '/recommend/songs'
        resp = self.default_request_get(url = url,need_login=True)
        return resp
    
    def search_songs(self,keywords : str = 'Luminous Memory',limits : int = 30, offset : int = 0):
        '''
        Search your query song based on keyword.
        keywords: Your query keywords, mainly songname, e.g. Never Gonna Give You Up.
        limits: Optional, decide how many songs will appear in one page, default = 30.
        offset: Optional, decide start from which result, default = 0.
        '''
        url = '/cloudsearch'
        resp = self.default_request_get(url = url, need_login = False, keywords = keywords, limits = limits, offset = offset)
        return resp

    def get_user_playlist(self,user_id : int):
        '''
        Find playlist of a user,
        user_id : Must, the user you want to find.
        '''
        url = "/user/playlist"
        resp = self.default_request_get(url = url, need_login=True, uid = user_id)
        return resp

    def get_playlist_all(self,list_id : int,limit : int = None,offset : int = 0):
        '''
        Find all music given a playlist.
        list_id : Must, the list you want to find.
        limit : Optional, how many tracks will return at one time.
        offset : Optional, it will start at which track.
        '''
        url = '/playlist/track/all'
        resp = self.default_request_get(url = url,need_login=True,id = list_id,limit = limit, offset = offset)
        return resp

    def get_like_playlist(self,user_id : int):
        '''
        Find 'like' playlist of a user.
        user_id : Must, the user you want to find.
        '''
        resp = self.get_user_playlist(user_id=user_id)
        if resp['playlist'] == []:
            logger.warning("Cannot Fetch playlist, maybe the user set perimissions on privacy.")
            return False
        else:
            list_id = resp['playlist'][0]['id']
            resp = self.get_playlist_all(list_id)
            return resp