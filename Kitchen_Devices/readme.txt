This is the repository for the MMI 19/20 smart kitchen intelligent AI virtual agent.

Guide for starting RFID-Devices:

Raspberry Pi IP Adressen:
192.168.0.37 - Utensilienschrank (sollte funktionieren, noch nicht getestet)
192.168.0.38 - Topfschrank
192.168.0.39 - Vorrat (Kabelproblem wrsl)
192.168.0.40 - Geschirrschrank
192.168.0.41 - Besteckkasten

Raspberry Pi Zugangsdaten(für alle gleich):
Username: pi
password: pi

Client Script (Read.py) automatisch beim hochfahren des Raspberrys ausführen (ERLEDIGT):
1. Per SSH mit dem Raspberry Pi verbinden
2. Das File /etc/rc.local mit öffnen: "sudo nano /etc/rc.local"
3. Vor das "exit 0" Zeile einfügen: "sudo nano /home/pi/pi-rfid/Read.py &"
4. Strg+O zum abspeichern, Strg+X zum schließen -> Fertig!

Anleitung zum Starten des Setups:
1. Deaktivieren der Windows Firewall oder ähnlichem (blockiert meistens die Requests)
2. Verbinden des Laptops mit dem Router: SSID: "FRITZ!Box WLan 3370", Pw:"4208918844837754"
3. Eigene IP Adresse abfragen. In der Kommandozeile "ipconfig" oder im Router nachschaun
4. Start "main.py" -> In der Konsole müsste "Listening on: '' ... " erscheinen
5. Starten aller Raspberry Pis
6. Überprüfen im Router, ob alle Raspberry Pis mit dem Router verbunden sind ("fritz.box" im Browser)
7. Sich mit jedem Raspberry verbinden über Putty(Einfach IP Adresse der PIs eingeben) und folgende Schritte durchführen:
    - Directory wechseln: "cd pr-rfid"
    - Read.py öffnen: "sudo nano Read.py"
    - Die Host-Ip Adresse zu der zuvor abgefragtem IP Adresse (zu der IP Adresse des Rechners welcher die main.py ausführt)
    ändern
    - Datei Speicher: "strg+o"
    - Raspberry neu starten: "sudo reboot now"

-> Hoffen das es funktioniert!!

Replay des LSL Streams (BEISPIEL):
python D:\Studium\MMI-19-20\LSL_Replay\lsl_replay.py D:\Studium\MMI-19-20\LSL_Replay\Lab_Recordings.xdf