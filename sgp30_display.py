import busio, board, adafruit_ssd1306
import os, sys, time, datetime, stat, subprocess, json
from PIL import Image, ImageDraw, ImageFont

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
font = ImageFont.truetype('FreeMono.ttf', 18)
disp.fill(0)
disp.show()

def setupDisplay():
  width = disp.width
  height = disp.height
  image = Image.new('1', (width, height))
  draw = ImageDraw.Draw(image)
  draw.text((2, 2), 'Starting...', font=font, fill=255)
  disp.image(image)
  disp.show()

def closeDisplay():
  width = disp.width
  height = disp.height
  image = Image.new('1', (width, height))
  draw = ImageDraw.Draw(image)
  draw.text((2, 2), 'Shutdown.', font=font, fill=255)
  disp.image(image)
  disp.show()


def updateDisplay(c, v):
  padding = 2
  width = disp.width
  height = disp.height
  image = Image.new('1', (width, height))
  draw = ImageDraw.Draw(image)
  draw.rectangle((0,0,width,height), outline=0, fill=0)
  x = padding
  top = padding
  if c < 0:
    draw.text((x, top),    '%d' % -c, font=font, fill=255)
  else:
    draw.text((x, top),    'eC02 %5d' % c, font=font, fill=255)
    draw.text((x, top+22), 'TVOC %5d' % v, font=font, fill=255)
  now = datetime.datetime.now()
  draw.text((x, top+44), now.strftime("%H:%M:%S"), font=font, fill=255)
  disp.image(image)
  disp.show()

setupDisplay()

mqttXtraArgs = []
mqttDest = "localhost"
if 'MQTT_HOST' in os.environ:
  mqttXtraArgs.extend('-h', os.environ['MQTT_HOST'])
  mqttDest = os.environ['MQTT_HOST']

def pub(topic, payload):
  subprocess.run(['mosquitto_pub', '-t', topic, '-m', payload] + mqttXtraArgs, stdout=subprocess.PIPE)

def getBaseline(baselineFile):
  if not os.path.exists(baselineFile):
    return None
  try:
    f = open(baselineFile, 'r')
    b1 = f.readline()
    b2 = f.readline()
    f.close()
    return [int(b1), int(b2)]
  except:
    pass
  return None

print("This assumes read_sgp30 -i already ran")

# n = 0
# while(n > 0):
#   time.sleep(1)
#   n = n - 1
#   updateDisplay(-n, 0)
#   print(n, "    \r", end="", flush=True)
# print("\r     \r", end="", flush=True)

result = subprocess.run(['ReadSGP30/build/bin/read_sgp30', '-s'], stdout=subprocess.PIPE)
value = result.stdout.decode()
data = json.loads(value)
serial = data['serial_number']

topic = 'pib/sgp30/' + serial

print("MQTT topic=%s, destination=%s" % (topic, mqttDest))

baselineFile = os.path.join(os.environ['HOME'], '.lr_read_sgp30', 'baseline.txt')
cmd = 'ReadSGP30/build/bin/read_sgp30'

if os.path.exists(baselineFile):
  rc = subprocess.run([cmd, '-xr'], stdout=subprocess.PIPE)

baseline = getBaseline(baselineFile)
if baseline is not None:
  pub(topic, '{"baseline":[%d,%d]}' % (baseline[0], baseline[1]))
  print("baseline=", baseline[0], baseline[1])

ready = False
sys.stdout.flush()
time.sleep(1)
t0 = time.perf_counter() 
try:
  while True:
    result = subprocess.run([cmd], stdout=subprocess.PIPE)
    value = result.stdout.decode()
    data = json.loads(value)
    CO2 = data['co2_ppm']
    TVOC = data['tvoc_ppb']
    payload = json.dumps(data, separators = (',', ':'))
    pub(topic, payload)
    t1 = time.perf_counter()
    dt = t1 - t0
    print("CO2=", CO2, "TVOC=", TVOC)
    if not ready:
      sys.stdout.flush() # https://unix.stackexchange.com/a/285511
      if 'NOTIFY_SOCKET' in os.environ:
        subprocess.run(['systemd-notify', '--ready'])
      ready = True
    updateDisplay(CO2, TVOC)
    if dt / 60 / 60 >= 1.0:
      print("Saving updated baseline")
      rc = subprocess.run([cmd, '-xs'], stdout=subprocess.PIPE)

      baseline = getBaseline(baselineFile)
      if baseline is not None:
        pub(topic, '{"baseline":[%d,%d]}' % (baseline[0], baseline[1]))
    time.sleep(5)

finally:
  closeDisplay()

