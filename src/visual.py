import sys
import io
import smbus
from time import sleep
from struct import unpack
import numpy as np
import audioop
import threading


# Return power array index corresponding to a particular frequency
def piff(val):
  return int(4 * chunksize * val/sample_rate)

global bus
bus = smbus.SMBus(0)

# Initialize the arrays
global weighting # Change these according to taste
weighting = [1, 1.5, 3, 4, 6.5, 9]
# Precalculate weighting bins
weighting = np.true_divide(weighting, 1000000)

# audio settings
sample_rate = 48000
no_channels = 1 # mono only
global chunksize
chunksize = 2048

# stdin acts as a file, read() method
global stdin
stdin  = getattr(sys.stdin, 'buffer', sys.stdin)

print("Loading...")
global data
data = stdin.read(chunksize*5)

print("Playing...")
#output.write(data)

counter = 0

def leftloop():
  binsl       = [0,0,0,0,0,0]
  counterl = 0
  color = [0,0,0]

  while data!='':
    datal = audioop.tomono(stdin.read(chunksize), 2, 0, 4)
    npdatal = np.array(unpack("%dh"%(len(datal)/2), datal), dtype='h')
    fourierl = np.fft.rfft(npdatal)
    fourierl = np.delete(fourierl, len(fourierl) -1)
    powerl = np.abs(fourierl)
  
    lower_boundl = 0
    upper_boundl = 64

    for i in range(len(binsl)):
      meanl = np.mean(powerl[piff(lower_boundl) : piff(upper_boundl):1])
      binsl[i] = int(meanl) if np.isnan(meanl) == False else 0
      if counterl == 0:
        print([piff(lower_boundl), piff(upper_boundl)])
      lower_boundl = upper_boundl
      upper_boundl = upper_boundl << 1


    binsl = np.divide(np.multiply(binsl,weighting),5)

    for i in range(6):
      if binsl[i]*720 > 0 and binsl[i]*720 < 85:
        color = [0,255,0]
      elif binsl[i]*720 > 85 and binsl[i]*720 < 170:
        color = [0,0,255]
      elif binsl[i]*720 > 170 and binsl[i]*720 < 255:
        color = [255,0,0]
      bus.write_i2c_block_data(0x13, i, color)

    counterl += 1

def rightloop():
  binsr       = [0,0,0,0,0,0] 
  counterr = 0
  color = [0,0,0]

  while data!='':
    datar = audioop.tomono(stdin.read(chunksize), 2, 4, 0)
    npdatar = np.array(unpack("%dh"%(len(datar)/2), datar), dtype='h')
    fourierr = np.fft.rfft(npdatar)
    fourierr = np.delete(fourierr, len(fourierr) -1)
    powerr = np.abs(fourierr)
  
    lower_boundr = 0
    upper_boundr = 64

    for i in range(len(binsr)):
      meanr = np.mean(powerr[piff(lower_boundr) : piff(upper_boundr):1])
      binsr[i] = int(meanr) if np.isnan(meanr) == False else 0
      if counterr == 0:
        print([piff(lower_boundr), piff(upper_boundr)])
      lower_boundr = upper_boundr
      upper_boundr = upper_boundr << 1


    binsr = np.divide(np.multiply(binsr,weighting),5)
    print([binsr[0],binsr[1],binsr[2],binsr[3],binsr[4],binsr[5]])

    for i in range(6):
      if binsr[i]*680 > 0 and binsr[i]*680 < 85:
        color = [0,255,0]
      elif binsr[i]*680 > 85 and binsr[i]*680 < 170:
        color = [0,0,255]
      elif binsr[i]*680 > 170 and binsr[i]*680 < 255:
        color = [255,0,0]
      bus.write_i2c_block_data(0x13, 11-i, color)

    counterr += 1

threading.Thread(target=leftloop).start()
threading.Thread(target=rightloop).start()

print("Finished")

