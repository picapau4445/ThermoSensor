#!/usr/bin/env python

# ASW Iot lib
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging

# conf
import awsIotMessageConf as conf

class AwsIotMessage:
    
    # client connection instance
    myAWSIoTMQTTClient = None

    # Custom MQTT message callback
    def customCallback(self, client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

    def connect(self):
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
        endpoint = conf.endpoint
        connectDevicePackageDir = conf.connect_device_package_dir
        rootCAPath = connectDevicePackageDir + conf.root_ca_file_name
        privateKeyPath = connectDevicePackageDir + conf.private_key_file_name
        certificatePath = connectDevicePackageDir + conf.certificate_file_name

        self.myAWSIoTMQTTClient = None
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient(conf.client_id)
        self.myAWSIoTMQTTClient.configureEndpoint(endpoint, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        # Connect and subscribe to AWS IoT
        return self.myAWSIoTMQTTClient.connect()

    def subscribe(self):
        #myAWSIoTMQTTClient.subscribe(conf.topic, 1, self.customCallback) # arg2 "1" is QoS1
        return

    def publish(self, payload):
        return self.myAWSIoTMQTTClient.publish(conf.topic, payload, 1) # arg3 "1" is QoS1

    def disconnect(self):
        self.myAWSIoTMQTTClient.disconnect()
