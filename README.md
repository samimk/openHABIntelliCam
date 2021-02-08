# openHABIntelliCam
Jetson Nano-based intelligent security camera for openHAB

This project uses Nvidia Jetson Nano with pre-trained detection model (defaults to SSD-Mobilenet-v2) for detecting persons. Each detection is reported by MQTT to openHAB (or other) MQTT broker, and then used for indicating detection on openHAB's Basic UI or HAB Panel. Notification of detections are sent to openHAB cloud instance.
