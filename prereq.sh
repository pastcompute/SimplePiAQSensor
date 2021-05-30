sudo apt install mosquitto_clients python3-pip gcc cmake i2c-tools
pip3 install adafruit_circuitpython_sgp30
pip3 install adafruit_circuitpython_ssd1306
git clone https://github.com/LuckyResistor/ReadSGP30
cd ReadSGP30
mkdir -p buid
cd build
cmake ..
make
cd ../..
sudo ln -sf $(realpath AQSensor.service) /etc/systemd/system/AQSensor.service
