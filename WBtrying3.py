#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, session, flash
import socket
from functools import wraps


app = Flask(__name__)
table_light_status = 0
solder_light_status = 0
blue_light_status = 0
big_light_status = 0
door_status = 0

app.secret_key = "your_mom"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

@app.route('/opendoor')
def opendoor5():
    send("open_door5", "", 5002)
    return "<h1>door opened<h1>"


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():

    if request.method =='POST':
        global table_light_status
        global solder_light_status
        global blue_light_status
        global big_light_status
        global door_status
        device = request.form.get('device')
        status = int(request.form.get('status'))
        if device == "table_light":
            table_light_status = status
            signal_to_table_light(status)

        if device == "solder_light":
            solder_light_status = status
            signal_to_solder_light(status) 

        if device == "blue_light":
            blue_light_status = status
            signal_to_blue_light(status) 

        if device == "big_light":
            big_light_status = status
            signal_to_big_light(status) 

        if device == "door":
            door_status = status 
            signal_to_door(status)

    return render_template('index.html', table_light_status = "{s}" .format(s='ON' if table_light_status else 'OFF'),
                         solder_light_status = "{s}" .format(s='ON' if solder_light_status else 'OFF'),
                         blue_light_status = "{s}" .format(s='ON' if blue_light_status else 'OFF'),
                         big_light_status = "{s}" .format(s='ON' if big_light_status else 'OFF'),
                         door_status = "{s}" .format(s='OPEN' if door_status else 'CLOSED'))

def signal_to_door(state):
    if (state):
        send("open_door", "", 5002)
    else:
        send("close_door", "", 5002)

def signal_to_table_light(state):
    if (state):
        send("table_light_on", "", 5002)
    else:
        send("table_light_off", "", 5002)

def signal_to_solder_light(state):
    if (state):
        send("solder_light_on", "", 5002)
    else:
        send("solder_light_off", "", 5002)

def signal_to_big_light(state):
    if (state):
        send("big_light_on", "", 5002)
    else:
        send("big_light_off", "", 5002)

def signal_to_blue_light(state):
    if (state):
        send("blue_light_on", "", 5002)
    else:
        send("blue_light_off", "", 5002)

def send1(message, address, port):
        #print (message)
        s = socket.socket()
        host = address
        port = port
        s.connect((host,port))
        s.send(message)
        s.close()

def send(message, address, port):
        send1(message,address,port)
        sendLog(message);

def sendLog(String):
        message = 'LocalWP___%s'% (String)
        send1(message, "", 5007)



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password' :
            error = 'Invalid user'
        else:
            session['logged_in'] = True
#            flash('You were just logged in!')
            return redirect (url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
        session.pop('logged_in', None)
#        flash('You were just logged out!')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3141, debug=True)
