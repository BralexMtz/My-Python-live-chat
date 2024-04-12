import socketio
from socketio.exceptions import TimeoutError
import time

def main():
  username=input("username: ")
  with socketio.SimpleClient() as sio:
    sio.connect('http://127.0.0.1:5000')
    print('my sid is', sio.sid)
    print('my transport is', sio.transport)
    sio.emit('join', {'username': username})

    event = sio.receive()
    
    if len(event[1]['usuarios']) > 1:
      print(event[1])
      for user in event[1]['usuarios']:
        if user != username:
          print(user, "esta activo")
          username_to=user
      message_to=input("> ")
      sio.emit('message', {'username_to': username_to,'message':message_to})
    else:
      print("Esperando otro usuario ...")
    
    while True:
      time.sleep(2)
      event = sio.receive()
      if 'message' in event[1].keys():
        user_from=event[1]['message']['name_from']
        message=event[1]['message']['message']
        print(f"[{user_from}]: {message} ")
        message_to=input("> ")
        sio.emit('message', {'username_to': event[1]['message']['name_from'],'message':message_to})
      

    print("ends")


if __name__ == "__main__":
  print("connecting to server...  127.0.0.1:5000")
  
  main()
