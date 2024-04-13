import socketio
from socketio.exceptions import TimeoutError
import time

def handler_message(sio,data):
  user_from=data['name_from'] 
  message=data['message']['message']

  print(f"[{user_from}]: {message} ") # imprime el mensaje recibido como chat
  message_to=input("> ") # nos pide un mensaje para responder
    
  sio.emit('message', {'username_to': user_from,'message':message_to}) # se envia el mensaje de respuesta al otro usuario

def handler_usuarios(sio,data,username):
  if len(data['usuarios']) > 1: # si hay más de 1 usuario vemos su nombre de usuario y empieza el chat
    print(data)
    for user in data['usuarios']:
      if user != username:
        print(user, "esta activo")
        username_to=user # asigna el username para empezar el chat
    message_to=input("> ") #escribir mensaje
    sio.emit('message', {'username_to': username_to,'message':message_to}) # se envia el mensaje al usuario con su mensaje
  else: # si solo es 1 usuario (el primero) esperamos a que se conecte alguien mas
    print("Esperando otro usuario ...")

def main():
  username=input("username: ") # pedimos nombre de usuario
  with socketio.SimpleClient() as sio:
    sio.connect('http://127.0.0.1:5000') # ip y puerto del servidor socket
    print('my sid is', sio.sid) # id dado por el socket
    print('my transport is', sio.transport)
    sio.emit('join', {'username': username}) # creamos una bandeja de entrada/room para recibir mensajes con nuestro username

    event = sio.receive() # esperamos a recibir algún evento 
    if 'usuarios' in event[1].keys():
      handler_usuarios(sio,event[1],username)
    
    while True:
      time.sleep(2)
      event = sio.receive() # esperamos un mensaje del socket
      if 'message' in event[1].keys(): # si el evento del socket tiene un mensaje en sus datos
        handler_message(sio,event[1]['message'])
      elif 'usuarios' in event[1].keys(): # si el evento del socket tiene usuarios
        handler_usuarios(sio,event[1],username)
    print("ends")


if __name__ == "__main__":
  print("connecting to server...  127.0.0.1:5000")
  
  main()
