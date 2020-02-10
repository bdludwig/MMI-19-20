#!/usr/bin/env python3

import socket
from threading import Thread
import time
import pickle
import selectors


class SocketServer(Thread):

    def __init__(self, host, port, myKitchen):
        self.host = host
        self.port = port
        self.kitchen = myKitchen
        self.sel = selectors.DefaultSelector()

        self.sock = socket.socket()
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print('Listening on', (host, port))
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, self.accept)

        Thread.__init__(self)
        self.daemon = True
        self.start()

    def accept(self, sock, mask):
        conn, addr = sock.accept() # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        data = conn.recv(1024) # Should be ready
        if data:
            print('Recieved', repr(data), 'from', conn)
            # Do more Stuff...
            data = pickle.loads(data)
            self.kitchen.updateTool(data)
        else:
            print('closing', conn)
            self.sel.unregister(conn)
            conn.close()

    def run(self):
        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)


