import sys
import os
import socket
import errno
from socket import error as socket_error
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
import time
from EPD import EPD

WHITE = 1
BLACK = 0

# fonts are in different places on Raspbian/Angstrom so search
possible_fonts = [
    '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',            # Debian B.B
    '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf',   # Debian B.B
    '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono-Bold.ttf',   # R.Pi
    '/usr/share/fonts/truetype/freefont/FreeMono.ttf',                # R.Pi
    '/usr/share/fonts/truetype/LiberationMono-Bold.ttf',              # B.B
    '/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf'               # B.B
]


FONT_FILE = ''
for f in possible_fonts:
    if os.path.exists(f):
        FONT_FILE = f
        break

if '' == FONT_FILE:
    raise 'no font file found'

IP_FONT_SIZE = 25
NOTE_FONT_SIZE = 15

def main(argv):
    """main program - draw current IP address on 2.70" size panel"""

    epd = EPD()

    print('panel = {p:s} {w:d} x {h:d}  version={v:s}  cog={g:d}'.format(p=epd.panel, w=epd.width, h=epd.height, v=epd.version, g=epd.cog))

    if 'EPD 2.7' != epd.panel:
        print('incorrect panel size')
        sys.exit(1)

    epd.clear()

    demo(epd)

def demo(epd):
    """simple drawing demo - show used IP address"""

    # initially set all white background
    image = Image.new('1', epd.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)
    width, height = image.size

    ip_font = ImageFont.truetype(FONT_FILE, IP_FONT_SIZE)
    note_font = ImageFont.truetype(FONT_FILE, NOTE_FONT_SIZE+1)

    # clear the display buffer
    draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
    previous_day = 0

    # display image on the panel
    epd.display(image)
    epd.update()

    first_error = True
    last_show_ip = '--'
    new_found_ip = '++'
    delay_for_next = 2

    while True:
        while True:
            try:
                #print("In loop trying")
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                #print("non-blocking")
                s.setblocking(0)
                #print("got socket")
                s.connect(("8.8.8.8",80))
                #print("connected")
                new_found_ip = s.getsockname()[0]
                s.close()
                first_error = True
                delay_for_next = 5
                break;
            except socket_error as serr:
                # Failed connection
                if first_error:
                    draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
                    draw.text((10, 10), 'Not Connected', fill=BLACK, font=ip_font)
                    draw.text((10, 40), 'Error {code:d}'.format(code=serr.errno))
                    first_error = False
                    last_show_ip = '--'
                    delay_for_next = 2

                    # display image on the panel
                    epd.display(image)
                    epd.update()

                print('Failed to connect, error {code:d}'.format(code=serr.errno))
            time.sleep(delay_for_next)

        if last_show_ip != new_found_ip:
            print('last "{last:s}" new "{n:s}"'.format(last=last_show_ip, n=new_found_ip))
            #draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
            draw.rectangle((1, 1, width - 1, height - 1), fill=WHITE, outline=BLACK)
            draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
            draw.text((10, 10), 'IP ADDR:', fill=BLACK, font=note_font)
            draw.text((10, 25), '{ip:s}'.format(ip=new_found_ip), fill=BLACK, font=ip_font)
            draw.text((10, 55), 'GATEWAY:', fill=BLACK, font=note_font)
            draw.text((10, 70), '255.255.255.255', fill=BLACK, font=ip_font)
            last_show_ip = new_found_ip

            # display image on the panel
            epd.display(image)
            epd.update()
        else:
            print('Testing again in {delay:d}s'.format(delay=delay_for_next))
            time.sleep(delay_for_next)
            #delay_for_next = delay_for_next * 2
            #if delay_for_next > 30:
            #    delay_for_next = 30

# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass
