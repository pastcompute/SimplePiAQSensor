# Raspberry Pi CO2 sensor

This project provides a wrapper around [ReadSGP30](https://github.com/LuckyResistor/ReadSGP30) on any Raspberry Pi (will work on an Pi or Pi Zero, including the original Pi A/B), displaying the sensor value on an OLED display and also publishing the data on MQTT.

Tested using an original Pi B 512MB and Raspbian 10.

## Installation and Use

This assumes a fresh install of Raspbian 10 and the pi will be dedicated to this application.

- prepare a Raspberry Pi. It works on even an original Pi A or B with a USB Wifi adaptor, although it will be slow to install and debug.
- most recently I am running this on a new Pi 3B
- after booting a fresh SD card, run `sudo raspi-config`
  - setup your Wifi
  - I also run in console only mode
  - ensure you enable i2c, and enabling SSH is very helpful when debugging
- checkout this repository in /home/pi
- connect the SGP30 and SSD1306 to the Pi i2c bus
- install the [prerequisites](./prereq.sh)
- enable & start the systemd service
- the first time let the device run outside if possible for 12-24 hours to gain an accurate baseline
- as required, test the MQTT connection using `mosquitto_sub -t 'aqsensor/#'`
- this configuration by default is insecure, use at your own risk

## Customisation

- use the environment variable `MQTT_TOPIC`, this defaults to `aqsensor` and is appended with `/` and the serial number of the sensor
- send direct to an extenal MQTT server using `MQTT_HOST`; at the moment it uses the default port with `mosquitto_pub` 
- environment variables are set in the file `AQSensor.service`

## Maintenance

- the baseline info is saved in `/home/pi/.lr_read_sgp30/baseline.txt`
- to force it to be reset on next reboot run `touch /home/pi/AQSensor/reset-baseline.flag` (or just delete the directory)
- to send to an alterantive MQTT service (default is localhost) set the environment variable `MQTT_HOST` in the service file

## Todo

- document the pin connections, etc.
