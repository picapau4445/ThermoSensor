#!/usr/bin/env python

# raspi lib
import RPi.GPIO as GPIO
import spidev
import time
from datetime import datetime

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
    spi.open(0,0) # select ADC/MCP3008 : bus=0, CE=0
    return spi

def temp_read(adc, ch):
    buf = adc.xfer2([1,((8+ch)<<4),0]) # read adc data
    adResult = ((buf[1]&3)<<8)+buf[2] # select data
    volt= adResult * 3.3 / 1024.0 # converte data to Voltage
    temp = (volt*1000.0 - 500.0)/10.0 # convertr volt to temp
    return temp

if __name__ == ("__main__"):

    # raspi adc init
    adc= adc_init()
    channel=0 # select CH0 : ADC/MCP3008

    # raspi gpio init
    gpio_init(conf.gpiono1)

    interval = interval1

    # raspi temperature read 
    while (True):
    #for i in range():
        gpio_on(conf.gpiono1);
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        temp = temp_read(adc, channel)
        message = '{"temperature": ' + str(temp) + ', "recDate": "' + now + '", "deviceId": "ohashi_raspi_modelB"}'
        print "temperature = ", str(temp) 
        print "humidity = ", "comming soon!"
        print "message = ", message
        time.sleep(interval)

    adc.close()
