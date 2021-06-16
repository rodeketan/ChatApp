import os

from collections import deque

from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from helpers import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "my secret key"
socketio = SocketIO(app)

channelsCreated = []


usersLogged = []
users={}


channelsMessages = dict()

@app.route("/")
@login_required
def index():

    return render_template("index.html", channels=channelsCreated)

@app.route("/signin", methods=['GET','POST'])
def signin():
    ''' Save the username on a Flask session
    after the user submit the sign in form '''


    session.clear()

    username = request.form.get("username")

    if request.method == "POST":

        if len(username) < 1 or username == '':
            return render_template("error.html", message="username can't be empty.")

        if username in usersLogged:
            return render_template("error.html", message="that username already exists!")

        usersLogged.append(username)



        session['username'] = username


        session.permanent = True

        return redirect("/")
    else:
        return render_template("signin.html")

@app.route("/logout", methods=['GET'])
def logout():
    """ Logout user from list and delete cookie."""


    try:
        usersLogged.remove(session['username'])
    except ValueError:
        pass


    session.clear()

    return redirect("/")

@app.route("/create", methods=['GET','POST'])
def create():
    """ Create a channel and redirect to its page """


    newChannel = request.form.get("channel")

    if request.method == "POST":

        if newChannel in channelsCreated:
            return render_template("error.html", message="that channel already exists!")


        channelsCreated.append(newChannel)


        channelsMessages[newChannel] = deque()

        return redirect("/channels/" + newChannel)



@app.route("/channels/<channel>", methods=['GET','POST'])
@login_required
def enter_channel(channel):
    """ Show channel page to send and receive messages """


    session['current_channel'] = channel

    if request.method == "POST":

        return redirect("/")
    else:
        return render_template("channel.html", channels= channelsCreated, messages=channelsMessages[channel])

@socketio.on("joined", namespace='/')
def joined():
    """ Send message to announce that user has entered the channel """


    room = session.get('current_channel')
    users[session.get('username')]=request.sid

    join_room(room)

    emit('status', {
        'userJoined': session.get('username'),
        'channel': room,
        'msg': session.get('username') + ' has entered the channel'},
        room=room)

@socketio.on("left", namespace='/')
def left():
    """ Send message to announce that user has left the channel """

    room = session.get('current_channel')

    leave_room(room)

    emit('status', {
        'msg': session.get('username') + ' has left the channel'},
        room=room)

@socketio.on('send message')
def send_msg(msg, timestamp):
    """ Receive message with timestamp and broadcast on the channel """


    room = session.get('current_channel')

    # Save 100 messages and pass them when a user joins a specific channel.

    if len(channelsMessages[room]) > 100:
        # Pop the oldest message
        channelsMessages[room].popleft()

    channelsMessages[room].append([timestamp, session.get('username'), msg])

    emit('announce message', {
        'user': session.get('username'),
        'timestamp': timestamp,
        'msg': msg},
        room=room)
###############Personal Touch########
@socketio.on('private_message', namespace='/private')
def private_message(payload):
    recipient_session_id = users[payload['username']]
    message = payload['message']
    room=session.get('username')+payload['username']
    socketio.server.enter_room(users[session.get('username')], room, namespace='/private')
    socketio.server.enter_room(recipient_session_id, room, namespace='/private')



    emit('new_private_message', {
        'user': session.get('username'),
        'msg': message}, room=room)
