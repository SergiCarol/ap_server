#!/usr/bin/env python
import time
import os, pty, serial
import requests
import json
import logging

logging.basicConfig(filename='serial.log', filemode='w', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

SERVER = "http://157.230.107.10:5000"
API_KEY = "O0waAcEEmlRqQZBb2m69VjzpeKJCIfxzpATpfpZbI-U"

ser = serial.Serial(
        port='/dev/ttyACM0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

while True:
    serial_data = ser.readline().decode("utf-8") 
    if serial_data == '':
        continue
    print("Data from serial port: ", serial_data)
    if serial_data == "data start\r\n":
        request = ser.readline().decode("utf-8")
        request.replace("\r\n", "")
        
        request = json.loads(request)
        print("Data for request: ", request)

        r = requests.post(SERVER + '/upload', json=json.dumps(request))
        print("Request response: ", r.json())
        response_data = r.json()
        ser.write(str(response_data).encode())
        ser.write(bytes(b'!'))

