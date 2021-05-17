# Raspberry Pi CO2 sensor

This project provides a wrapper around [ReadSGP30](https://github.com/LuckyResistor/ReadSGP30) on any Raspberry Pi (will work on an Pi or Pi Zero, including the original Pi A/B), displaying the sensor value on an OLED display and also publishing the data on MQTT.

Tested using an original Pi B 512MB and Raspbian 10.

## Installation and Use

- connect the SGP30 and SSD1306 to the Pi i2c bus
- install the [prerequisites](./prereq.sh)
- enable & start the systemd service
- the first time let the device run outside if possible for 12-24 hours to gain an accurate bseline

## Todo

- document the pin connections, etc.
- test prereq.sh, it has only been assembled from my shell history
