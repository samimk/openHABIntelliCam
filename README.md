# openHABIntelliCam
Jetson Nano-based intelligent security camera for openHAB

This project uses Nvidia Jetson Nano with pre-trained detection model (defaults to SSD-Mobilenet-v2) for detecting persons. Each detection is reported by MQTT to openHAB (or other) MQTT broker, and then used for indicating detections on openHAB's Basic UI or HAB Panel. Notification of detections are sent to openHAB cloud instance.

Reports are sent as JSON with single field:
{
"Person": 1 #or# 0
}

## Installation
1. Copy intellicam.py to Jetson Nano.
2. Configure parameters in intellicam.py.
3. Add a new channel to MQTT Thing in openHAB Paper UI and create new item.
4. Add the newly created item to Basic UI or HAB Panel.
5. Copy rule file intellicam.rule to /etc/openhab2/rules
6. Configure notification settings in intellicam.rule.
