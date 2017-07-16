#!/usr/bin/env python

import sys

# raspi lib
import RPi.GPIO as GPIO
import spidev
import time

# AwsIot lib
import AwsIotLib.awsIotMessage as aws

# conf
import thermoSensorConf as conf

# Payload format
import thermoSensorPayload as payloadFormatter

def gpio_init(gpiono):
    GPIO.setmode(GPIO.BOARD) #use GPIO Number
    GPIO.setup(gpiono, GPIO.OUT)

def gpio_on(gpiono):
    GPIO.output(gpiono,GPIO.HIGH)

def gpio_off(gpiono):
    GPIO.output(gpiono,GPIO.LOW)

def spi_init():
    spi=spidev.SpiDev() # genarate spi instance
    spi.open(conf.adc_bus,conf.adc_ce) # select ADC/MCP3008 : bus=0, CE=0
    return spi

def temperature_read(adc, ch):
    buf = adc.xfer2([1, ((8 + ch) << 4), 0]) # read adc data
    adResult = ((buf[1]&3) << 8) + buf[2] # select data
    volt= adResult * 3.3 / 1024.0 # converte data to Voltage
    temperature = (volt * 1000.0 - 500.0) / 10.0 # convertr volt to temp
    return temperature

if __name__ == ("__main__"):

    # raspi spi init
    spi = spi_init()

    # raspi gpio init
    gpio_init(conf.gpio_no)
    gpio_on(conf.gpio_no);

    # AWS IoT init
    aws_iot_msg_client = aws.AwsIotMessage()
    if aws_iot_msg_client.connect():
        print "connected."
    else:
        print "connection error."
        sys.exit(1)

    # raspi temperature read 
    while (True):
        temperature = temperature_read(spi, conf.mcp9700_channel)
        payload = payloadFormatter.getPayloadString(conf.device_id, str(temperature))
        print "temperature = ", str(temperature) 
        print "humidity = ", "humidity"
        print "payload = ", payload

        if aws_iot_msg_client.publish(payload):
            print "payload published."
        else:
            print "publish error."

        time.sleep(float(conf.interval))

    # not reached.
    #spi.close()
    #aws_iot_msg_client.disconnect()
