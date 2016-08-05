from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import datetime
import os



WHITE = 1
BLACK = 0
FONTSIZE_BIG = 20
FONTSIZE_STAMP = 15
BORDER  = 3
INTERLINE = 3
STAMPSTRIPE = 15
STAMP_OFFSET = 65
IP_COMMAND = "sudo ifconfig ARG | grep 'inet addr:' | sed 's/^.*inet addr://' | cut -b 1-14"
MAC_COMMAND = "sudo ifconfig ARG | grep 'HWaddr ' | sed 's/^.*HWaddr //' | cut -b 1-17"

def EPD_ip(epd):

# define characteristic points of EPD

#_________________________________________
#|a ----->X           b                 c|
#| Y|                                    |
#|  |                                    |
#|  V                                    |
#|                                       |
#|d                   e                 f|
#|                                       |
#|                                       |
#|                                       |
#|____________________h__________________|
#|g             STAMPSTRIPE             i|
#|j_____________________________________k|


    a_y = 0
    a_x = 0
    b_y = 0
    b_x = epd.width / 2
    c_y = 0
    c_x = epd.width
    d_y = ( epd.height - STAMPSTRIPE ) / 2
    d_x = 0
    e_y = ( epd.height - STAMPSTRIPE) / 2
    e_x = epd.width / 2
    f_y = ( epd.height - STAMPSTRIPE ) / 2
    f_x = epd.width
    g_y = epd.height - STAMPSTRIPE
    g_x = 0
    h_y = epd.height - STAMPSTRIPE
    h_x = epd.width / 2
    i_y = epd.height - STAMPSTRIPE
    i_x = epd.width
    j_y = epd.height
    j_x = 0
    k_y = epd.height
    k_x = epd.width
    
    epd.clear()
    
    # define fonts 
    font_value=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", FONTSIZE_BIG)
    font_stamp=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", FONTSIZE_STAMP)
        
    # initially set all white image and image in the background
    image = Image.new('1', epd.size, WHITE)
 
    # prepare for drawing
    draw = ImageDraw.Draw(image)
    
    conns = [ 'eth0', 'wlan0' ]

    x_pos = a_x
    y_pos = a_y
    
    for conn in conns:
        #change the commands to apply to the specified connection
        ip_command = IP_COMMAND.replace("ARG", conn)
        mac_command = MAC_COMMAND.replace("ARG", conn)
        
        # obtain the IP address with use ofe predefined system COMMAND
        ip = os.popen(ip_command).read()
        ip = ip[0:len(ip)-1] # delete the EOL character 
    
        # do the same for the MAC address
        MAC = os.popen(mac_command).read()
        MAC = MAC[0:len(MAC)-1]
        
        draw.text( (x_pos, y_pos), conn, fill=BLACK, font=font_value)
        y_pos = y_pos + FONTSIZE_BIG + INTERLINE
        draw.text( (x_pos, y_pos),'IP: %s' % ip, fill=BLACK, font=font_value)
        y_pos = y_pos + FONTSIZE_BIG + INTERLINE
        draw.text( (x_pos, y_pos), 'MAC: %s' % MAC, fill=BLACK, font=font_value)
        y_pos = y_pos + 2*FONTSIZE_BIG + INTERLINE
      
    
    # draw stampstripe line
    draw.line( [ ( g_x, g_y ),( i_x, i_y ) ], fill=BLACK)
         
    # put the timestamp
    draw.text( (STAMP_OFFSET, h_y), '{:%d/%m/%Y %H:%M:%S}'.format(datetime.datetime.now()), fill=BLACK, font = font_stamp)
    
    # display image on the panel
    epd.display(image)
    epd.update()
        
        