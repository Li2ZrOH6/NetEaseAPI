# In order to complete my PyDL homework.
# I wonder it's necessary to make a simple backend structure for a website.
# Based on flask + Jinja2.

from dataFetcher import NetEaseAPI
import re,json
from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)
api = NetEaseAPI()

@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        if request.form.get('submit') == 'Login':
            return redirect(url_for('login'))
        elif request.form.get('submit') == "No login":
            return redirect(url_for('search'))
    return render_template('index.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    error1,error2 = False,False
    mode = 0
    if request.method == 'POST':
        uid = request.form.get('uid')
        if re.search(r"@163.com$",uid) == None:
            if re.search(r'^1[0-9]{10}$',uid) == None:
                error1 =  "Invalid Uid."
            else:
                mode = 2
        else:
            mode = 1
        if mode != 0:
            pwd = request.form.get('pwd')
            return_value = api.login(mode,pwd,id = uid)
            if type(return_value) == tuple:
                user_profile = return_value[1]
                uid = user_profile['account']['id']
                with open(f'profile/profile_{uid}.json','w') as fp:
                    json.dump(user_profile,fp)
                return redirect(url_for('show_user_profile',uid = uid,is_login = True))
            elif return_value == 2:
                error2 =  "False PWD or UID"
            else:
                error2 = "Login Failed."  
        print(error1,error2)
    return render_template('login.html',error1 = error1,error2 = error2)

@app.route('/profile/<int:uid>',methods = ['GET','POST'])
def show_user_profile(uid):
    with open(f'profile/profile_{uid}.json','r') as fp:
        profile = json.load(fp)
        user_name = profile['profile']['nickname']
        avatar_url = profile['profile']['avatarUrl']
        bg_url = profile['profile']['backgroundUrl']
    if request.method == 'POST':
        if request.form.get('submit') == 'Recommend Music':
            return redirect(url_for('recommend_songs'))
        elif request.form.get('submit') == "My Playlist":
            return redirect(url_for('test2'))
        elif request.form.get('submit') == "My Likes":
            return redirect(url_for('test2'))
        elif request.form.get('submit') == "Search Music":
            return redirect(url_for('search'))
    return render_template('profile.html',user_name = user_name, avatar_url = avatar_url, bg_url = bg_url)

@app.route('/recommend')
def recommend_songs():
    result = api.get_recommend_songs()
    if result == False:
        return 'Please Login First!'
    else:
        return render_template('recommend.html',songList = result['data']['dailySongs'])

@app.route('/search',methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        songList = api.search_songs(keywords=query)
        if songList != False:
            songList = songList['result']['songs']
            return render_template('recommend.html',songList = songList)
    return render_template('search.html')

@app.route('/test2')
def test2():
        return 'This is test2.'

if __name__ == '__main__':
    app.run()