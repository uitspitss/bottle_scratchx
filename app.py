#!python
#-*-coding:utf-8-*-
#Time-stamp: <Wed Jan 13 20:57:15 JST 2016>
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division


# for bottle
import os
from bottle import route, run, template, request, response, static_file

# for scratchx
import usb
import sys
sys.path.append("..")
from arduino.usbdevice import ArduinoUsbDevice
import random

theDevice = None

@route("/")
def top():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title></title>
</head>
<body>
  <a href="http://scratchx.org/?url=http://localhost:5000/main.js">ScratchX</a>
</body>
</html>
'''

@route("/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="./")

@route("/blink")
def blink():
    theDevice = ArduinoUsbDevice(idVendor=0x16c0, idProduct=0x05df)

    red = request.query.get('red')
    green = request.query.get('green')
    blue = request.query.get('blue')

    print("red:{}, green:{}, blue:{}".format(red, green, blue))

    red = int(mapping(red))
    green = int(mapping(green))
    blue = int(mapping(blue))

    theDevice.write(ord("s"))
    theDevice.write(red)
    theDevice.write(green)
    theDevice.write(blue)

    print("mred:{}, mgreen:{}, mblue:{}".format(red, green, blue))

def mapping(arg):
    arg = float(arg)
    if arg < 0:
        return 0
    elif arg > 100:
        return 255
    else:
        return arg * 0.01 * 255

if __name__ == '__main__':
    run(host="localhost", port=5000, debug=True, reloader=True)

