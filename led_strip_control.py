# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import argparse
from neopixel_plus import NeoPixel
import math

# LED strip configuration:
LED_COUNT = 150  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.addressable_strip_length):
        strip.leds[i] = color
        strip.write()
        time.sleep(wait_ms / 1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.addressable_strip_length, 3):
                strip.leds[i + q] = color
            strip.write()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.addressable_strip_length, 3):
                strip.leds[i + q] = 0


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return pos * 3, 255 - pos * 3, 0
    elif pos < 170:
        pos -= 85
        return 255 - pos * 3, 0, pos * 3
    else:
        pos -= 170
        return 0, pos * 3, 255 - pos * 3


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.addressable_strip_length):
            strip.leds[i] = wheel((i + j) & 255)
        strip.write()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.addressable_strip_length):
            strip.leds[i] = wheel((int(i * 256 / strip.addressable_strip_length) + j) & 255)
        strip.write()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.addressable_strip_length, 3):
                strip.leds[i + q] = wheel((i + j) % 255)
            strip.write()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.addressable_strip_length, 3):
                strip.leds[i + q] = 0


def showWithGeom(leds, strip):
    real_len = 90
    leds = leds[0:real_len]
    if len(leds) != real_len:
        leds.extend([(255, 255, 255) for _ in range(real_len - len(leds))])
    for i in range(28):
        strip.leds[i] = leds[10 + i]
    for i in range(36, 60):
        strip.leds[i] = leds[59 - i]
    for i in range(60, strip.addressable_strip_length):
        strip.leds[i] = leds[i - 60]
    strip.write()

def linearGradient(colorA, colorB, strip, length):
    leds = []
    for i in range(length):
        leds.append((colorA[0] - i * (colorA[0] - colorB[0]) / length,
                             (colorA[1] - i * (colorA[1] - colorB[1]) / length),
                             (colorA[2] - i * (colorA[2] - colorB[2]) / length)))
    print(leds)
    showWithGeom(leds, strip)

def breathingGradient(colorA, colorB, strip, length, period):
    numberOfValues = 256
    while(1):
        for i in range(numberOfValues):
            k = (math.sin(2 * math.pi * i / numberOfValues) + 1) / 2
            linearGradient((colorA[0] * k, colorA[1] * k, colorA[2] * k), (colorB[0] * k, colorB[1] * k, colorB[2] * k), strip, length)
            time.sleep(period / numberOfValues)



# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-l', '--light', action='store_true', help='Light up the strip with predefined fixed pattern')
    parser.add_argument('-t', '--test', action='store_true', help='Light one led at a time to show the index of each led')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    # strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    # strip.begin()

    strip = NeoPixel(pin_num=LED_PIN,
                     n=LED_COUNT,
                     test=False,
                     overwrite_line=False,
                     target="adafruit")

    try:
        if args.light:
            linearGradient((0, 255, 0), (255, 0, 0), strip, 90)
            # breathingGradient((255, 0, 0), (0, 255, 0), strip, 90, 0.001)
        if args.clear:
            strip.fadeout()
        if args.test:
            for i in range(strip.addressable_strip_length):
                input(i)
                strip.leds[i] = (255, 255, 255)
                strip.write()



            # for i in range(150):
            #     strip.leds[i] = (255, 0, 0)
            #     strip.write()
            #     strip.leds[i] = (0, 0, 0)
            #     print(i)
            #     input()

            #     print('Color wipe animations.')
            #     colorWipe(strip, (255, 0, 0))  # Red wipe
            #     colorWipe(strip, (0, 255, 0))  # Blue wipe
            #     colorWipe(strip, (0, 0, 255))  # Green wipe
            #     print('Theater chase animations.')
            #     theaterChase(strip, (127, 127, 127))  # White theater chase
            #     theaterChase(strip, (127, 0, 0))  # Red theater chase
            #     theaterChase(strip, (0, 0, 127))  # Blue theater chase
            #     print('Rainbow animations.')
            #     rainbow(strip)
            #     rainbowCycle(strip)
            #     theaterChaseRainbow(strip)


    except KeyboardInterrupt:
        if args.clear:
            strip.fadeout()
