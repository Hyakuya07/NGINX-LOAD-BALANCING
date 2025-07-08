from flask import Flask, render_template, request, Response, send_from_directory, send_file
from datetime import datetime, timezone, timedelta
import mysql.connector as mysql
import logging
log = logging.getLogger('werkzeug')
log.disabled = True

db = mysql.connect(
    host='host.docker.internal',
    user='root',
    port = 3306,
    password='idonotknowthisdatabase',
    database='nginxappdb'
)
cursor = db.cursor()

import socket
container_id = socket.gethostname()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey, do not share this with anyone, it is a secret!, do not share this with anyone, it is a secret!, do not share this with anyone, it is a secret!'

def reroute_to(target):
    r = Response(status=302)
    r.headers.add("Location", target)
    return r

@app.route('/js/<filename>')
def handle_js_get(filename):
    return send_file("templates/js/" + filename)
    

@app.route('/logout')
def logout():
    print("Handling logout ")
    color = request.cookies.get('colorchoice',"red")
    r = Response(render_template('login.html', colorchoice=color), status=200)
    r.headers.add('Set-Cookie','user=;')
    return r
    

@app.route('/')
def home():   
    print("Handling /")
    color = request.cookies.get('colorchoice',"red") 
    user =  request.cookies.get('user', '')
    if user:
        return reroute_to('/dash')
    else:
        return render_template('login.html',colorchoice=color)

@app.route('/dash', methods = ["POST","GET"])
def dash():
    print("Handling /dash")
    usern = request.cookies.get("user", '')
    color = request.cookies.get("colorchoice", 'blue')
    cookies = False
    if usern:
        cookies=True
    else:
        usern = request.form.get('username','')
        passw = request.form.get('password', '')
        color = request.form.get('colorchoice', 'blue')
        cursor.execute("SELECT username, password FROM users WHERE username = %s AND password = %s", (usern, passw))
        if cursor.fetchone() is None:
            Flag = False
        else:
            Flag = True
    if cookies or (Flag):
        r = Response(render_template('home.html', user=usern, colorchoice=color, id = container_id), status=200)
        expirestime = datetime.now(timezone.utc) + timedelta(seconds=10)
        expirestr = expirestime.strftime("%a %d %b %Y %H:%M:%S UTC; ")
        cookiestr = f"user={usern};expires=" + expirestr
        cookie2str = f"colorchoice={color};"
        #WED 1 Oct 2015 07:28:00 GMT
        r.headers.add('Set-Cookie', cookiestr)
        r.headers.add('Set-Cookie', cookie2str)
        return r
    else:
        return reroute_to('/')

if __name__ == "__main__":      
    app.run(port=5000)