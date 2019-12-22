#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522

def sample_func(sample_var):
    # Beispiel Funktion
    # Skript starten, Daten loggen, etc.
    print("Test Funktion wurde aufgerufen")

# ...

MIFAREReader = MFRC522.MFRC522()
authcode = [114, 97, 115, 112, 98, 101, 114, 114, 121] # die ersten 9 Ziffern sind der Authentifizierungscode

try:
    while True:
        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()
            # This is the default key for authentication
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)
            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                # Read block 8
                data = MIFAREReader.MFRC522_Read(8)
                if data[:9] == authcode:
                    sample_func(data)
                #elif ...

except KeyboardInterrupt:
    print("Abbruch")
    GPIO.cleanup()