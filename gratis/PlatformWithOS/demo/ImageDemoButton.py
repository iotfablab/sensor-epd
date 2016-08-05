# Copyright 2013 Pervasive Displays, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#   http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.


import sys
import os
import time
from PIL import Image
from PIL import ImageOps
from EPD import EPD
import RPi.GPIO as GPIO

button_has_been_pressed = False

def main(argv):
    """main program - display list of images"""

    # The display adapter has a button connected to pin 15
    # on the RaspberryPi pin list. Pin 15 is BCM GPIO22,
    # where BCM stands for Broadcom SoC.
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(22, GPIO.FALLING, callback=button_pressed, bouncetime=300)

    epd = EPD()

    epd.clear()

    print('panel = {p:s} {w:d} x {h:d}  version={v:s}'.format(p=epd.panel, w=epd.width, h=epd.height, v=epd.version))

    for file_name in argv:
        if not os.path.exists(file_name):
            sys.exit('error: image file{f:s} does not exist'.format(f=file_name))
        print('display: {f:s}'.format(f=file_name))
        display_file(epd, file_name)

    GPIO.remove_event_detect(22)

def button_pressed(channel):
    """callback from GPIO when the button is pressed"""
    
    global button_has_been_pressed
    button_has_been_pressed = True
    

def button_sleep(max_seconds):
    """sleeps up to max_seconds or until user presses the button"""

    global button_has_been_pressed
    x = max_seconds * 10
    while x > 0:
        x -= 1
        if button_has_been_pressed:
            button_has_been_pressed = False
            break
        time.sleep(0.1)

def display_file(epd, file_name):
    """display centre of image then resized image"""

    image = Image.open(file_name)
    image = ImageOps.grayscale(image)

    # crop to the middle
    w,h = image.size
    x = w / 2 - epd.width / 2
    y = h / 2 - epd.height / 2

    cropped = image.crop((x, y, x + epd.width, y + epd.height))
    bw = cropped.convert("1", dither=Image.FLOYDSTEINBERG)

    epd.display(bw)
    epd.update()


    button_sleep(3) # delay in seconds

    rs = image.resize((epd.width, epd.height))
    bw = rs.convert("1", dither=Image.FLOYDSTEINBERG)

    epd.display(bw)
    epd.update()

    button_sleep(3) # delay in seconds

# main
if "__main__" == __name__:
    if len(sys.argv) < 2:
        sys.exit('usage: {p:s} image-file'.format(p=sys.argv[0]))
    main(sys.argv[1:])
