#!/usr/bin/python3

from flask import Flask, render_template
import subprocess
import _thread
from flask_socketio import SocketIO
from time import sleep

app = Flask(__name__, template_folder=".")
app.config['SECRET_KEY'] = "demosocketkey"
app.config
socketio = SocketIO(app)


def sendIPFSupdates(noop):
    ipfs = ""  # IPFS ref to file that IPNS address points to
    while True:

        socketio.emit('update', {"data": "/ipfs/QmYGozMdxye5GpU9G2MqPRd4p3Njqbw15Gqzh5zsuznHcy"},broadcast=True)
        sleep(2)
        socketio.emit('update', {"data": "/ipfs/QmVgf8nBY6uMKV4ai1nkhPhRUEx5nt5Pcopaz7v8wrWmU8"},broadcast=True)
        sleep(2)
        
    while True:    
        print(":: resolving ")
        # Hardcoded demo key, from the key file included in the repo
        ipfs2 = subprocess.run(["ipfs.exe", "name", "resolve", "QmYyNEaMs1LjnZSQvc4uCAU2JXyFqLb3K1MfiMy3tEgjnY"],
                                stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        print(":: Resolved to:", ipfs2)
        # If the file has changed
        if ipfs != ipfs2:
            ipfs = ipfs2
            print(":: Updated the ipfs var")
            # Tell the client - it will update the iframe img with the new url
            socketio.emit('update', {"data": ipfs},broadcast=True)
            print(":: Told the client")
        sleep (2)


@app.route("/")
def mainpage():

    print(":: rendered homepage")
    return render_template("home.html")


# The client sends a "success" message once it has connected
@socketio.on("success")
def on_success(message):
    # Now the client is connected, the IPNS polling can begin
    print(":: Started update loop")
    _thread.start_new_thread( sendIPFSupdates,("",) )
 

if __name__ == '__main__':
    socketio.run(app)  # Runs the production eventlet server unless in dev mode

