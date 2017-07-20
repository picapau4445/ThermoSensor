#!/usr/bin/env python

from datetime import datetime

def getPayloadString1(device_id, temperature):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    payload = '{' + \
              '"temperature": ' + temperature + ', ' + \
              '"recDate": "' + now + '", ' + \
              '"deviceId": "' + device_id + '" ' + \
              '}'
    return payload

def getPayloadString2(device_id, temperature, humidity):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    payload = '{' + \
              '"temperature": ' + temperature + ', ' + \
              '"humidity": ' + humidity + ', ' + \
              '"recDate": "' + now + '", ' + \
              '"deviceId": "' + device_id + '" ' + \
              '}'
    return payload
