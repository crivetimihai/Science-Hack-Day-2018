#!/usr/bin/env python3

from picamera import PiCamera
from time import sleep
from datetime import datetime as dt

camera = PiCamera()
direc = "/tmp/"


def i_name():
    curr_time = dt.now().strftime("%y%m%d%H%M%S")
    i_name = curr_time+".png"
    return i_name


def get_image():
    iname = i_name()
    idir = direc+iname
    print(idir)
    sleep(1)
    camera.capture(idir)
    #
    with open(idir,'rb') as fimage:
        f = fimage.read()
        b = bytearray(f)
    return b



