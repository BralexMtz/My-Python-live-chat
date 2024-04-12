from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds" # llave secreta que usa flask
socketio = SocketIO(app)

clients={} # almacenamos la relacion de ids(generada por los sockets) y el nombre de usuario

@socketio.on('join')
def on_join(data):
    print("joining")
    username=data['username']
    clients[request.sid]=username # se agrega como un nuevo cliente habilitado para chatear
    print(clients) 
    join_room(username) # se crea como una bandeja de entrada o room para que reciba mensajes este usuario
    print(f"{username} created their room")
    # Después notificamos a todos los clientes que usuarios hay disponibles con una lista de usernames
    data={"usuarios":[ username for username in list(clients.values())]} 
    send(data, broadcast=True) # enviamos un mensaje broadcast a todos con los usuarios
    

@socketio.on("message")
def message(data):    
    content = { # se crea la estructura del mensaje recibido
                'message':{ # con esta llave el cliente sabe que es un mensaje
                    "name_from": clients[request.sid], # obtenemos el nombre de usuario de quien envia con el sid
                    "message": data["message"], # agregamos mensaje 
                    "name_to": data['username_to'] # agregamos destinatario
                    }
              }
    send(content, to=data['username_to']) # se envia el diccionario del mensaje a su bandeja de entrada / room
    print(f"{content['message']['name_from']} said: {content['message']['message']} to {data['username_to']}")

@socketio.on("connect")
def connect(auth):# aqui se puede autenticar con algún token si se necesitara
    print(f"{request.sid} connects")

@socketio.on("disconnect")
def disconnect(): # cuando el cliente cierra sesión llega aqui 
    if request.sid in clients.keys(): # valida que este entre los clientes registrados para mensajear
      name=clients[request.sid]
      print(name,"bye") 
      leave_room(name) # se elimina su bandeja de entrada / room
      del clients[request.sid]

    
    
    # print(f"{name} has left the room")

if __name__ == "__main__":
    socketio.run(app, debug=True)