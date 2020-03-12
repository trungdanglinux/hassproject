# hassproject

This project uses Home Asisstant platform, Raspberry Pi and some devices such sensors, relay, LEDs, Camera.
The purpose is to monitor the stove in the kitchen and make an action to keep it safe when it intends to burn.

Specifically, user left a working stove when cooking. System will detect the smoke from the a pot or pan. it will turn off the stove immediately. Sometimes user even forget turns off stove when pot and pan are not in use. System can detect the high temperature and turn it off.

For the hardware, there are two pieces of Raspberry Pi 3, two LEDs, a relay, a rpi camera,LCD and many sensors such as motion sensor, smoke sensor,flame sensor, temperature and humidity sensor DHT11.
For the software, image HassOS is installed in Raspberry Pi and Raspbian OS is in another Raspberry Pi 3.

Installation:
 - All the sensors and devices are attached to the Rasbperry Pi ports which runs HassOS while rpi camera is connected to the one with Raspbian.
 - A relay with a red LED acts like switching a stove. The camera is connected to home assistant as IP camera via wifi with a support of motion package in Raspbian OS:
      - $sudo apt-get install motion
      - Configuring file in /etc/motion/motion.conf
      - Also change the option start_motion_daemons=no to start_motion_daemons=yes in /etc/default/motion
      -$sudo systemctl start motion
      - check if it works by puting IP address of Raspberry and port on browser address <IP address:port> (8081 by default)
 - For home assistant, the system can be monitored and controlled via web user interface with IP address and the port with the systax <IP address:8123> or using DNS <hassio.local:8123>. The system can monified in /config/configuration.yaml via SSH (secure shell) and also automated in automations.yaml.
