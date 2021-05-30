#!/bin/bash
set -e

# Note, mosquitto is optional, it runs a local MQTT service which is connected to by default
sudo apt-get install -y mosquitto-clients python3-pip gcc cmake i2c-tools python3-pip python3-pil mosquitto
pip3 install adafruit_circuitpython_sgp30
pip3 install adafruit_circuitpython_ssd1306
test -e ReadSGP30/.git || git clone https://github.com/LuckyResistor/ReadSGP30
cd ReadSGP30
mkdir -p build
cd build
cmake ..
make
cd ../..
sudo ln -sf $(realpath AQSensor.service) /etc/systemd/system/AQSensor.service
