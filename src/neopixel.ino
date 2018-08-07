#include <Wire.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif
#define PIN            6
#define NUMPIXELS      12
#define SLAVE_ADDRESS 0x04

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
byte a[4] = {0,0,0,0};
int delayval = 50;
int i,j=0, flag = 0;
void setup()
{
  pixels.begin();
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
}

void loop()
{
 delay(100);
}

void receiveEvent(int byteCount)
{
    i = 0;
    while(Wire.available())    // slave may send less than requested
    { 
      byte c = Wire.read(); // receive a byte as character
      a[i] = c;
      i++;
    }
    pixels.setPixelColor(a[0], pixels.Color(a[1],a[2],a[3]));
    pixels.show();
    //delay(delayval);
}

