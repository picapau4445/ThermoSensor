#!/usr/bin/env python

import sys

# raspi lib
import RPi.GPIO as GPIO
import spidev
import time

# DHT11 lib
import DHT11_Python.dht11 as dht11

# GY30 lib
import GY30Lib.luxSensor as gy30

# AwsIot lib
import AwsIotLib.awsIotMessage as aws

# conf
import thermoSensorConf as conf

# Payload format
import thermoSensorPayload as payloadFormatter

def gpio_init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) #use GPIO Number

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

    # raspi gpio init
    gpio_init()

    # DHT11 init
    dht11_instance = dht11.DHT11(pin=conf.gpio_no)

    # GY30 init
    gy30_instance = gy30.GY30(conf.gy30_bus, conf.gy30_addr)

    # AWS IoT init
    aws_iot_msg_client = aws.AwsIotMessage()
    if aws_iot_msg_client.connect():
        print("connected.")
    else:
        print("connection error.")
        sys.exit(1)

    # raspi temperature read 
    while (True):
        result = dht11_instance.read()
        if result.is_valid():
            # DHT11 temperature & humidity
            temperature = result.temperature
            humidity = result.humidity
            print("Temperature: %d C" % temperature)
            print("Humidity: %d %%" % humidity)

            # GY30 lux
            lux = gy30_instance.read
            print("Lux: %d" % lux)

            payload = payloadFormatter.getPayloadString3(conf.device_id, str(temperature), str(humidity), str(lux))
            print("payload = ", payload)
            
            if aws_iot_msg_client.publish(payload):
                print("payload published.")
            else:
                print("publish error.")

        else:
            print("Error: %d" % result.error_code)


        time.sleep(float(conf.interval))

    # not reached.
    #spi.close()
    #aws_iot_msg_client.disconnect()
