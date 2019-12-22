# Tracking objects via RFID chips

In order to track objects in the kitchen the idea was to equip the objects with RFID chips or cards and to place RFID readers in storage objects like cupboards.

As readers RFID RC522 Shields are used which are connected to Raspberry Pis.  

----------

Requirements for reading/writing RFIDs with a Raspberry Pi:
1.  Edit raspberry config for using SPI Bus:
    ```bash
    $ sudo nano /boot/config.txt
    device_tree_param=spi=on
    dtoverlay=spi-bcm2708
    // Save and close with Ctrl+O and Ctrl+X
    ```
2.  Activate SPI and reboot:
    ```bash
    $ sudo raspi-config
    //  „Advanced Options“ > „SPI“ > activate setting
    $ reboot now
    ```
3. Check if module is loaded:
    ```bash
   $ dmesg | grep spi
   [   10.784368] bcm2708_spi 20204000.spi: master is unqueued, this is deprecated
   [   10.813403] bcm2708_spi 20204000.spi: SPI Controller at 0x20204000 (irq 80)
    ```
4. Install python packages:
   ```bash
   $ sudo apt-get install git python-dev --yes
   ```
   Python SPI Module:
   ```bash
   $ git clone https://github.com/lthiery/SPI-Py.git
   $ cd SPI-Py
   $ sudo python setup.py install
   $ cd ..
   ```
    *** The following file has already been added to this repo. ***
    
    Raspberry Pi RFID RC522 module - python class which handles RFID reading and writing:
    
    (source is a python3 fork from: https://github.com/mxgxw/MFRC522-python)
   ```bash
   $ curl -OL https://raw.githubusercontent.com/lucassarcanjo/MFRC522-python/python3-spi-updates/MFRC522.py
   ```