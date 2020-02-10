#!/usr/bin/env python3

import socket
import pickle
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

HOST = '169.254.169.181'  # The server's hostname or IP address
PORT = 65432            # The port used by the server

while True:
    try:
        id, text = reader.read()

    finally:
        GPIO.cleanup()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        event = [str(id), "U_1_0"]
        print("Es passiert was")
        data = pickle.dumps(event)
        s.sendall(data)

    GPIO.cleanup()
    time.sleep(3)
