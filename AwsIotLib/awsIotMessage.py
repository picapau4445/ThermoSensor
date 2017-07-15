#!/usr/bin/env python

# ASW Iot lib
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging

class AwsIotMessage:
    
    # client connection instance
    myAWSIoTMQTTClient = None

    # Custom MQTT message callback
    def customCallback(client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

    def connect():
        # Configure logging
        '''
        logger = logging.getLogger("AWSIoTPythonSDK.core")
        logger.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        streamHandler.setFormatter(formatter)
        vlogger.addHandler(streamHandler)
        '''
        # Init AWSIoTMQTTClient
        host = "a3frmv98orkefb.iot.ap-northeast-1.amazonaws.com"
        connectDevicePackageDir = "/home/pi/connect_device_package/"
        rootCAPath = connectDevicePackageDir + "root-CA.crt"
        privateKeyPath = connectDevicePackageDir + "raspi_ohashi.private.key"
        certificatePath = connectDevicePackageDir + "raspi_ohashi.cert.pem"

        self.myAWSIoTMQTTClient = None
        self.mmyAWSIoTMQTTClient = AWSIoTMQTTClient("raspi_ohashi")
        self.mmyAWSIoTMQTTClient.configureEndpoint(host, 8883)
        self.mmyAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        # AWSIoTMQTTClient connection configuration
        self.mmyAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.mmyAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.mmyAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.mmyAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.mmyAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        # Connect and subscribe to AWS IoT
        self.mmyAWSIoTMQTTClient.connect()
        #myAWSIoTMQTTClient.subscribe("ohashiRaspiSensor", 1, customCallback)

    def publish(message):
        self.mmyAWSIoTMQTTClient.publish("ohashiRaspiSensor", message, 1)

    def disconnect():
        self.mmyAWSIoTMQTTClient.disconnect()
