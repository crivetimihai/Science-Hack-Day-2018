#!/usr/bin/env python3
"""
This module gets system information, hostname, and sensor data
from a Raspberry Pi with sensehat.
https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat
"""

import json
import socket
import subprocess
import re
from datetime import datetime
from sense_hat import SenseHat

# Parameters
PI_MODEL_FILE = '/proc/device-tree/model'
PI_TZ_FILE = '/etc/timezone'
PI_CPUTEMP_CMD = '/opt/vc/bin/vcgencmd measure_temp'

# Read data from config.py
from pihack.config import *

sense = SenseHat()

def show_message(txt):
    """ Displays text on RPI """
    sense.show_message(txt)
    return True

def get_timestamp():
    """Returns a timestamp in UTC timezone as a string

    >>> type(get_timestamp())
    <class 'str'>
    """
    return str(datetime.utcnow())

def get_temperature():
    """Average temperature in degrees Celsius from humidity and pressure sensor

    >>> temp1 = get_temperature()
    >>> (isinstance(temp1, float)) and (-50.0 <= temp1 <= 150.0)
    True
    """
    return((sense.get_temperature_from_humidity() + sense.get_temperature_from_pressure()) / 2)


def get_humidity():
    """Gets the percentage of relative humidity from the humidity sensor

    >>> isinstance(get_humidity(), float)
    True
    """
    return(sense.get_humidity())


def get_pressure():
    """Gets the current pressure in Millibars from the pressure sensor

    >>> isinstance(get_pressure(), float)
    True
    """
    return(sense.get_pressure())


def get_fqdn():
    """Returns the fully qualified domain name

    >>> get_fqdn()
    'raspberrypi'
    """
    return socket.getfqdn()


def get_tz():
    """Returns the timezone"

    >>> get_tz()
    'Etc/UTC'
    """

    with open(PI_TZ_FILE, 'r') as timezone_file:
        pi_tz = timezone_file.readline()
    return pi_tz.strip()


def get_pi_ver():
    """Returns the Raspberry Pi Version"

    >>> get_pi_ver()
    'Raspberry Pi 3 Model B Rev 1.2'
    """

    try:
        with open(PI_MODEL_FILE, 'r') as model_file:
            pi_ver = model_file.readline()
        return pi_ver.rstrip(' \t\r\n\0')
    except FileNotFoundError as error:
        return "{}. You're not running on a PI!".format(error)


def clean_temp(temp):
    """Extract only float temperature from data

    >>> clean_temp("9.39 degrees Celsius")
    9.39

    >>> type(clean_temp("9.39C"))
    <class 'float'>
    """
    return float(re.search("\d+\.\d+", temp).group())


def get_cpu_temp():
    """Returns the Raspberry Pi CPU Temperature

    >>> type(get_cpu_temp())
    <class 'float'>
    """
    # Check if the command returns a temperature.. if not, return an error?
    stdout_data = subprocess.getoutput(PI_CPUTEMP_CMD)
    return clean_temp(stdout_data.split()[0])


def get_corrected_temp():
    """Returns corrected temperature readings

    >>> type(get_corrected_temp())
    <class 'float'>
    """
    temp = get_temperature()
    cpu_temp = get_cpu_temp()
    temp_calibrated = temp - ((cpu_temp - temp)/5.466) - 5
    return temp_calibrated

def get_pi_info():
    """Returns Pi data and sensor information as JSON

    >>> json.loads(get_pi_info())
    {...}
    """
    pi_info = {
        'uuid'           : UUID,
        'location'       : LOCATION,
        'latitude'       : LATITUDE,
        'longitude'      : LONGITUDE,
        'sealevel'       : SEALEVEL,
        'sensorid'       : SENSORID,
        'project'        : PROJECT,
        'engineers'      : ENGINEERS,
        'timestamp'      : get_timestamp(),
        'fqdn'           : get_fqdn(),
        'tz'             : get_tz(),
        'pi_ver'         : get_pi_ver(),
        'cpu_temp'       : get_cpu_temp(),
        'temperature'    : get_temperature(),
        'corrected_temp' : get_corrected_temp(),
        'humidity'       : get_humidity(),
        'pressure'       : get_pressure()
    }
    return json.dumps(pi_info)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
    print(get_pi_info())
