# Copyright 2016 BIBA - Bremer Institut für Produktion und Logistik
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import datetime


WHITE = 1
BLACK = 0
FONTSIZE_SMALL = 14
FONTSIZE_BIG = 45
INTERLINE = 10
BORDER  = 3
STAMPSTRIPE = 15
STAMP_OFFSET = 65


def EPD_disp_3_val(epd, json_data):

# define characteristic points of EPD
#_________________________________________
#|a ----->X          |b                 c|
#| Y|                |                   |
#|  |   quad[0,0]    |     quad[0,1]     |
#|  V                |                   |
#|___________________|__________________ |
#|d                   e                 f|
#|                                       |
#|                quad[1,0]              |
#|                                       |
#|____________________h__________________|
#|g             STAMPSTRIPE             i|
#|j_____________________________________k|

    a_y = 0
    a_x = 0
    b_y = 0
    b_x = epd.width / 2
    c_y = 0
    c_x = 0
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
    
    # initially set all white image and image in the background
    image = Image.new('1', epd.size, WHITE)
    warning_sign = Image.open('./Images/warning_28x28.xbm', 'r')
    sign_width, sign_height = warning_sign.size

    # prepare for drawing
    draw = ImageDraw.Draw(image)
       
    # draw quadrant borders
    draw.line( [ ( b_x, b_y ),( e_x, e_y ) ], fill=BLACK)
    draw.line( [ ( d_x, d_y ),( f_x, f_y ) ], fill=BLACK)
    #draw stampstripe line
    draw.line( [ ( g_x, g_y ),( i_x, i_y ) ], fill=BLACK)

    # define fonts 
    font_label=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", FONTSIZE_SMALL)
    font_value=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", FONTSIZE_BIG)
   
    # encode the four quadrants into binary pairs
    list_of_quads=[ [0, 0], [0, 1], [1, 0] ]
    

    for quad in list_of_quads:
        
    #decode the binary pair into ident
        ident = quad[1]*1 + quad[0]*2
    # set upper left corner of the current quadrant
        xoffset = quad[1] * e_x
        yoffset = quad[0] * e_y
    # extract strings from .json records
        label = json_data[ident]["label"]
        value = json_data[ident]["value"]
    # get sizes for text centering 
        value_width, value_height = draw.textsize(value, font = font_value)
    # calculate the position of the left edge of the centered "value"
        y_cent_val = yoffset + ( epd.height / 2 - 1.2*value_height - sign_height - 2*BORDER) / 2 + sign_height

        if quad == [0, 0] or quad == [0, 1]:
            x_cent_val = xoffset + ( epd.width / 2 - value_width ) / 2    
        elif quad == [1, 0]:
            x_cent_val = ( epd.width - value_width ) / 2      
    # fill out the quadrant                    
        draw.text( (xoffset + BORDER, yoffset + BORDER) , '%s' %label, fill=BLACK, font=font_label)  
        draw.text( (x_cent_val, y_cent_val), '%s' %value, fill=BLACK, font=font_value)
        #draw a warning sign if the connection status is "false"
        if json_data[ident]["status"] == "false":
            if ident == 0 or ident == 1:
                image.paste(warning_sign,( e_x - sign_width + xoffset - BORDER, yoffset + BORDER))
            else:
                image.paste(warning_sign,( f_x - sign_width - BORDER, yoffset + BORDER))                
    # put the timestamp
    font_stamp=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 15)
    draw.text( (STAMP_OFFSET, h_y), '{:%d/%m/%Y %H:%M:%S}'.format(datetime.datetime.now()), fill=BLACK, font = font_stamp)
    
    # display image on the panel
    epd.display(image)
    epd.update()