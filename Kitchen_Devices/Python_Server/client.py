#!/usr/bin/env python3

import socket
import pickle
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432            # The port used by the server

while True:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        event = ["384192513797", "U_1_0"]
        data = pickle.dumps(event)
        s.sendall(data)
        # data = s.recv(1024)
        s.close()

    time.sleep(1)

#print('Received', repr(data))