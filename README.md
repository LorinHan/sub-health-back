# sub-health亚健康项目的后台

> 前端Vue + element-ui

## 后端采用flask开发，orm采用sqlalchemy。

---
# centos7下，部署flask + nginx + supervisor：
# 1.虚拟环境：pip install virtualenv
### 1.1 flask项目地址：/usr/local/flasky，只需要在项目地址下运行指令：
`virtualenv venv`
`source venv/bin/activate`
##### 退出虚拟环境的指令，直接敲：deactivate
### 1.2 直接把开发环境的flask依赖等导出为一个txt文件，然后在centos的虚拟环境中使用相应指令根据这个txt文件安装会非常方便
##### 如果无法导出依赖，先尝试推出虚拟环境再导出
`pip freeze >requerements.txt`
### 1.3 然后centos中使用以下指令
`pip install -r requerments.txt`
##### 这样就会在虚拟环境中安装一个与开发环境一致的副本了。注意一定要在虚拟环境中使用批量安装指令，不然就安装到全局去了，后果还是比较蛋疼的。
# 2.安装uWSGI
### 2.1 安装指令如下，注意一定要保证已经进入了虚拟环境并激活：
`pip install uwsgi`
### 2.2 直接在flask的根目录下面新建一个文件“config.ini”,使用的方式是配置启动。文件内容如下
```
[uwsgi]
 
# uwsgi 启动时所使用的地址与端口
# 如果不适用nginx，直接使用http的方式访问的话，下面的socket改为 http=0.0.0.0:80
socket = 127.0.0.1:5000
 
#虚拟环境目录 
home = /usr/local/flasky/venv
 
#指向网站根目录
chdir = /usr/local/flasky
 
#python启动程序文件
wsgi-file = manage.py
 
#python程序内用于启动的application变量名
callable = app
 
#处理器数
processes = 4
 
#线程数
threads = 2
 
#设置uwsgi包解析的内部缓存区大小。默认4k
 
buffer-size = 32768
```
### 2.3 配置文件的执行方式，命令行输入指令可以启动：
uwsgi config.ini
### 2.4 ctrl+c关闭程序，实际项目中我们的服务器上可能会有多个项目在运行，我们需要应用随同服务器启动并作为后台服务运行才是实际项目需要，所以我们需要安装另一个工具来引导执行uwsgi
# 3.安装supervisor
##### supervisor可以同时启动多个应用，最重要的是当某个应用down掉的时候，他可以自动重启该应用，保证可用性。
### 3.1 yum install supervisor
### 3.2 supervisor的全局配置文件在  /etc/supervisord.conf
##### 打开该默认配置文件，最下面一行我们看到，该默认配置文件会从 /etc/supervisord.d/ 目录下面加载所有的(*.ini)配置文件
### 3.3 我们不需要修改默认的配置文件，只需要在/etc/supervisord/目录下新建一个配置文件（命名为flask_supervisor.conf),该文件内容如下：
```
[program:flasky]
# 启动命令入口
command=/usr/local/flasky/venv/bin/uwsgi /usr/local/flasky/config.ini
 
# 命令程序所在目录
directory=/usr/local/flasky
#运行命令的用户名
user=root
 
autostart=true
autorestart=true
#日志地址
stdout_logfile=/usr/local/flasky/logs/uwsgi_super.log
```
##### autostart和autorestart参数保证了我们的应用可以一直保持启动的状态，即使是down掉了也能重启服务。
### 3.4 supervisor相关命令
```
supervisord -c /etc/supervisor.conf 启动

supervisorctl reload 	重启

supervisorctl reread	热重启
	supervisorctl update	

supervisorctl shutdown #关闭所有任务

supervisorctl stop|start program_name

supervisorctl status #查看所有任务状态
```
### 3.5 启动： supervisord -c /etc/supervisord.conf
##### supervisorctl status查看以一下状态，如果输出以下内容说明成功启动服务了
`项目名               RUNNING   pid 6416, uptime 0:23:42`
# 4. 安装Nginx
### 4.1 yum install nginx
### 4.2 找到nginx的配置文件，不要修改默认的nginx.conf（路径 /etc/nginx/nginx.conf）文件，只需要在同样的文件夹下面新建一个文件夹(conf.d)然后在conf.d下面新建配置文件（flask_ng.conf）即可,内容如下：
```
server {
  listen 80;
  server_name zehuo.huoran.net; #公网地址
 
  location / {
  include  uwsgi_params;
  uwsgi_pass 127.0.0.1:5000; # 指向uwsgi 所应用的内部地址,所有请求将转发给uwsgi 处理
  uwsgi_param UWSGI_PYHOME /usr/local/flasky/venv; # 指向虚拟环境目录
  uwsgi_param UWSGI_CHDIR /usr/local/flasky; # 指向网站根目录
  uwsgi_param UWSGI_SCRIPT manage:app; # 指定启动程序
  }
 }
```
### 4.3 service nginx start  或者  systemctl start nginx  启动nginx
### 4.4 netstat -ntl  查看nginx和uwsgi是否都启动了
# 5. 需要注意的是！在if __name__ == '__main__': main函数底下，只有一个app.run()的代码被uwsgi执行，main函数下的其他代码是不会被uwsgi执行的。。。大半天才找出这个坑。。
