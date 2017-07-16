#!/usr/bin/env python

import sys

# raspi lib
import RPi.GPIO as GPIO
import spidev
import time
from datetime import datetime

# AwsIot lib
import AwsIotLib.awsIotpayload as aws

# conf
import thermoSensorConf as conf

def gpio_init(gpiono):
    GPIO.setmode(GPIO.BOARD) #use GPIO Number
    GPIO.setup(gpiono, GPIO.OUT)

def gpio_on(gpiono):
    GPIO.output(gpiono,GPIO.HIGH)

def gpio_off(gpiono):
    GPIO.output(gpiono,GPIO.LOW)

def adc_init():
    spi=spidev.SpiDev() # genarate spi instance
    spi.open(conf.adc_bus,conf.adc_ce) # select ADC/MCP3008 : bus=0, CE=0
    return spi

def temperature_read(adc, ch):
    buf = adc.xfer2([1,((8+ch)<<4),0]) # read adc data
    adResult = ((buf[1]&3)<<8)+buf[2] # select data
    volt= adResult * 3.3 / 1024.0 # converte data to Voltage
    temperature = (volt*1000.0 - 500.0)/10.0 # convertr volt to temp
    return temperature

if __name__ == ("__main__"):

    # raspi adc init
    adc= adc_init()

    # raspi gpio init
    gpio_init(conf.gpio_no)

    # AWS IoT init
    aws_iot_msg_client = aws.AwsIotpayload()
    if aws_iot_msg_client.connect():
        print "connected."
    else:
        print "connection error."
        sys.exit(1)

    # raspi temperature read 
    while (True):
        gpio_on(conf.gpio_no);
        now = datetime.now().strftime(date_time_frmt)
        temperature = temperature_read(adc, conf.mcp9700_channel)
        payload = '{"temperature": ' + str(temperature) + ', "recDate": "' + now + '", "deviceId": "ohashi_raspi_modelB"}'
        print "temperature = ", str(temperature) 
        print "humidity = ", "comming soon!"
        print "payload = ", payload

        if aws_iot_msg_client.publish(payload):
            print "payload published."
        else:
            print "publish error."

        time.sleep(float(conf.interval))

    adc.close()
    aws_iot_msg_client.disconnect()
