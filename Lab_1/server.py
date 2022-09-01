from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import socket
from OpenSSL import SSL

port=8080
context = ('certs/cert.pem','certs/key.pem')
#context.use_privatekey_file('certs/key.pem')
#context.use_certificate_file(ç)
app = Flask(__name__)
socketio = SocketIO(app)

def broadcast(name, value):
	emit(name, value, broadcast=True, include_self=False)

@socketio.on('connect')
def test_connect():
	print('connected')
	emit('after connect',  {'data':'Lets dance'})



@socketio.on('emotion')
def handle_emotion(val):
	broadcast('emotion', val)

@socketio.on('audio')
def handle_audio(val):
	broadcast('audio', val)

@socketio.on('pauseAudio')
def handle_pause(val):	
	broadcast('pauseAudio', val)

@socketio.on('test')
def handle_test(val):	
	broadcast('test', val)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
# 	The way of getting the ip address is dumb but works https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
	print(f"access at http://{[ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith('127.')][0]}:{port}")
	socketio.run(app, host='0.0.0.0', debug=True, port=port,ssl_context=context)
