#!/usr/bin/env python

from bottle import static_file, route, run
from threading import Thread

import json
import asyncio
import websockets

from command.bot import Bot


connected = set()
host = 'sprint-hack.herokuapp.com'


def httpHandler():
    global host
    while True:
        @route('/')
        def index():
            static_file('index.css', root='./app')
            static_file('client.js', root='./app')
            return static_file("index.html", root='./app')

        @route('/<filename>')
        def server_static(filename):
            return static_file(filename, root='./app')

        run(host=host, port=9001)


@asyncio.coroutine
def receive_send(websocket, path):
    global connected
    # Please write your code here
    print("Receiving ...")
    connected.add(websocket)
    try:
        while True:
            data = yield from websocket.recv()

            send_data = '''{
            "data": "%s"
            }''' % data
            for ws in connected:
                yield from ws.send(send_data)

            send_data = Bot(data).run()
            send_data = json.dumps(send_data)

            for ws in connected:
                yield from ws.send(send_data)
    except KeyboardInterrupt:
        print('\nCtrl-C (SIGINT) caught. Exiting...')
    finally:
        connected.remove(websocket)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start_server = websockets.serve(receive_send, host, 3000)
    server = loop.run_until_complete(start_server)
    print('Listen')

    t = Thread(target=httpHandler)
    t.daemon = True
    t.start()

    try:
        loop.run_forever()
    finally:
        server.close()
        start_server.close()
        loop.close()
