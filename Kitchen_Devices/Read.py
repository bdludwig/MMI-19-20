#!/usr/bin/env python3

import socket
import pickle
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432            # The port used by the server

while True:
    try:
        id, text = reader.read()
    finally:
        GPIO.cleanup()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            event = [str(id), "Geschirrschrank"]
            data = pickle.dumps(event)
            s.sendall(data)
    except socket.error as msg:
        print(msg)

    time.sleep(3)
