from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


import uuid
import json
import uvicorn
import socketio
import eventlet


users = {}
names_from_tokens = {}
all_messages = []

app = FastAPI()

app.mount("/static", StaticFiles(directory="."))

@app.get("/prev")
def prev():
    return all_messages


@app.get("/login/{name}")
def login(name):
    token = str(uuid.uuid4())
    users[token] = True
    names_from_tokens[token] = name
    return {"token": token}


@app.get("/logout/{token}")
def logout(token):
    if token in users:
        users[token] = False
    
    return {"status_code": "ok"}
    

def backend_server():
    uvicorn.run(app, host='0.0.0.0', port=8000)



sio = socketio.Server(cors_allowed_origins='*')
capp = socketio.WSGIApp(sio)

@sio.event
def connect(sid, envoirn):
    print(sid, envoirn)

@sio.on('*')
def catch_all(event, sid, data):
    if event == "msg":
        d = json.loads(data)
        if d[0] in users and users[d[0]]==True:
            d[0] = names_from_tokens[d[0]]
            sio.emit('msg', json.dumps(d), broadcast = True)
            all_messages.append(d)

        else :
            print(f"message {data} dropped")
        


def chat_server():
    eventlet.wsgi.server(eventlet.listen(('', 8001)), capp)


if __name__ == "__main__":
    import threading
    t1 = threading.Thread(target=backend_server)
    t2 = threading.Thread(target=chat_server)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(0-0)

