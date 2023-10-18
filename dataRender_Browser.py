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
        # 处理按钮点击事件
        if request.form.get('submit') == 'Login':
            # 处理按钮1的逻辑
            return redirect(url_for('login'))
        elif request.form.get('submit') == "No login":
            # 处理按钮2的逻辑
            return redirect(url_for('test2'))
    return render_template('index.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        uid = request.form.get('uid')
        if re.search(r"@163.com$",uid) == None:
            if re.search(r'^1[0-9]{10}$',uid) == None:
                return "Invalid Uid."
            else:
                mode = 2
        else:
            mode = 1
        pwd = request.form.get('pwd')
        return_value = api.login(mode,pwd,id = uid)
        if type(return_value) == tuple:
            user_profile = return_value[1]
            uid = user_profile['account']['id']
            with open(f'profile/profile_{uid}.json','w') as fp:
                json.dump(user_profile,fp)
            return redirect(url_for('show_user_profile',uid = uid))
        elif return_value == 2:
            return "False PWD or UID"
        else:
            return "Login Failed."  
    return render_template('login.html')
"dailySongs"
@app.route('/logined/<int:uid>')
def show_user_profile(uid):
    with open(f'profile/profile_{uid}.json','r') as fp:
        profile = json.load(fp)
    return 'Hello,{}'.format(profile['profile']['nickname'])

@app.route('/recommend')
def recommend_songs():
    result = api.get_recommend_songs()
    print(result)
    if result == False:
        return 'Please Login First!'
    else:
        length = len(result['data']["dailySongs"])
        return 'Returned ' + str(length) + ' songs.'


@app.route('/test2')
def test2():
    try:
        return api.cookie_path
    except AttributeError:
        return 'This is test2.'

if __name__ == '__main__':
    app.run()