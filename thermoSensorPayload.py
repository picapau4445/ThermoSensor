#!/usr/bin/env python

from datetime import datetime

def getPayloadString(device_id, temperature):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    payload = '{"temperature": ' + temperature + ', "recDate": "' + now + '", "deviceId": "' + device_id + '"}'
    return payload
