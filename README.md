# NetEase API v0.1.0 Demo README

该项目是基于()[https://github.com/Binaryify/NeteaseCloudMusicApi]的一个前端代码实现。

~~同时是为了完成Python与深度学习作业而开始做的一个小Demo~~

其完成的功能接口 API 请参考上述网站，本项目仅仅在前端上实现了一小部分的功能。

且因赶时间，登录凭证将会在后面的开发中重做一下。

欢迎提issue，欢迎pr~

## 部署

1. 参考()[https://github.com/Binaryify/NeteaseCloudMusicApi]，在本机或服务器上部署后端
2. 将后端的（本地）IP地址填入`config.json`中的"server_address"项中，参见`config_example.json`。
3. 运行`dataRender_Browser.py`并访问挂载前端的地址。

## 功能实现

该项目的代码主要分为两部分：

```
dataFetcher.py
dataRender_Browser.py
```

前者（`dataFetcher.py`）主要完成了对源数据的获取，登录凭证cookie的储存。

后者主要是通过 `Flask + jinja2` 架构将其渲染在浏览器上。

### dataFetcher

该文件定义了一个名为`NetEaseAPI`的类，该类有以下方法：
- `__init__`：初始化，确认服务端地址和request访问头。
- `default_request_get`：通用的`get`函数，其传入`url`作为必须参数，并将`**kwargs`的键值对填入`request params`中
- `login`：通过输入手机-密码 / 163邮箱-密码进行登录，会临时存储登录cookie以维持状态。
- `login_check`：通过检查登录cookie以确认是否登录。
- `get_recommend_songs`：**仅登录可用**，获取当日日推歌单。
- `search_songs`：通过输入关键词搜索歌曲。
- `get_user_playlist`：**仅登录可用**，通过输入uid，获取某人的可见歌单和收藏歌单。
- `get_playlist_all`：通过输入歌单id，获取某个歌单的所有歌曲。
- `get_like_playlist`：**仅登录可用**，通过输入uid，获取某人的所有红心歌曲（如果可见）。

### dataRender（Browser）

`Flask + jinja2` 架构。

其主要完成了网站之间的交互。

同时完成了对返回结果的渲染。

主要路由如下：
- `/`：根目录，可以抵达登录网站和非登录功能网站。
- `/profile/<uid>`：展示了某个用户的资料
- `/login`：登录页面，相当于`api.login()`在浏览器上的实现。
- `/recommend`：在登陆后显示当日日推歌曲。
- `/search`：通过关键词搜索歌曲
- `/test2`：测试网站。（大雾）

### dataRender（PIL + go-cqhttp）

**Todo**

在QQbot上实现交互。