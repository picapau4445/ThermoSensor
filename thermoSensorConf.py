#!/usr/bin/env python

# for environ
import os

# GPIO Number
gpio_no = 29

# ADC/MCP3008 bus,CE
adc_bus=0
adc_ce=0

# ADC/MCP3008 - MCP9700 channel(0-7)
mcp9700_channel = 0

# GY30 bus, addr
gy30_bus=1
gy30_addr=0x23

# DHT11 retry parameter(sec)
dht11_retry_interval = 0.1
dht11_retry_count = 10

# temperature read interval(sec)
interval = 600

# deviceID for IoT message
device_id = "ohashi_raspi_modelB"