#!/usr/bin/python3

##################################################
## openHABIntelliCam
##################################################
#
# Jetson Nano-based security camera, which
# reports by MQTT when person detected
#
##################################################
## Author: Samim Konjicija
## Copyright: Copyright 2021, openHABIntelliCam
## Version: 0.0.1
## Maintainer: Samim Konjicija
## Email: skonjicija@etf.unsa.ba
##################################################

# imports
import time
import jetson.inference
import jetson.utils
import paho.mqtt.client as mqtt

# Start of openHABIntelliCam Settings

# MQTT broker setup
# openHAB MQTT broker IP address as string
MQTT_BROKER = ""
# openHAB MQTT broker port
MQTT_PORT = 1883
# openHAB MQTT broker user
MQTT_USER = ""
# openHAB MQTT broker password
MQTT_PASSWORD = ""
# openHAB MQTT broker topic for openHABIntelliCam
MQTT_TOPIC_ROOT = "smarthome/intellicam"

# Various settings
# video source for camera
VIDEO_SOURCE="/dev/video0"
# number of successive detections for setting alarm
COUNT = 3
# number of cycles for clearing alarm
COUNT1 = 50
# confidence of detection for setting alarm
CONFIDENCE=0.75
# minimum threshold for detection
THRESHOLD=0.5

# End of openHABIntelliCam Settings


DETECTION = False

def on_connect(client, userdata, flags, rc):
	print("{0}: Connected with result code {1}".format(time.asctime(),str(rc)))

def on_disconnect(client, userdata, rc):
	if rc != 0:
		print("{0}: Unexpected MQTT disconnection. Will auto-reconnect".format(time.asctime()))
	mqttclient.connect(MQTT_BROKER, MQTT_PORT, 60)

def on_message(client, userdata, msg):
	print("{0}: {1} - {2}".format(time.asctime(),msg.topic,str(msg.payload)))

mqttclient = mqtt.Client()
mqttclient.on_connect = on_connect
mqttclient.on_disconnect = on_disconnect
mqttclient.on_message = on_message
mqttclient.username_pw_set(MQTT_USER,MQTT_PASSWORD)

mqttclient.connect(MQTT_BROKER, MQTT_PORT, 60)

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=THRESHOLD)
camera = jetson.utils.videoSource(VIDEO_SOURCE)		# video source for snapshots
display = jetson.utils.videoOutput("display://0") 	# video stream display 

counter=0
counter1=0
while display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	for detection in detections:
		if detection.Confidence>CONFIDENCE:
			print("Class:"+net.GetClassDesc(detection.ClassID))
			if detection.ClassID==1:
				counter=counter+1
			if counter>COUNT:
				DETECTION=True
				mqttclient.publish(MQTT_TOPIC_ROOT, '{ "Person" : 1 }')
		counter1=counter1+1
	if counter1>COUNT1:
		counter1=0
		counter=0
		if DETECTION==True:
			mqttclient.publish(MQTT_TOPIC_ROOT, '{ "Person" : 0 }')
		DETECTION=False
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
