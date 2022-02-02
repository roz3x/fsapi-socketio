from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


import uuid
import uvicorn
import socketio
import eventlet


users = []
app = FastAPI()

app.mount("/static", StaticFiles(directory="."))

@app.get("/login/{name}")
def read_root(name):
    token = str(uuid.uuid4())
    users.append(token)
    return {"token": token}


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
        sio.emit('msg', data, broadcast = True)
        


def chat_server():
    eventlet.wsgi.server(eventlet.listen(('localhost', 8001)), capp)


if __name__ == "__main__":
    import threading
    t1 = threading.Thread(target=backend_server)
    t2 = threading.Thread(target=chat_server)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(0-0)

