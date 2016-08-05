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
from PIL import ImageOps
import datetime


WHITE = 1
BLACK = 0
FONTSIZE_SMALL = 25
FONTSIZE_BIG = 85
INTERLINE = 20
BORDER  = 5
STAMPSTRIPE = 15
STAMP_OFFSET = 5


def EPD_disp_1_val(epd, json_data):

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
    warning_sign = Image.open('./Images/warning.xbm', 'r')
    sign_width, sign_height = warning_sign.size

    # prepare for drawing
    draw = ImageDraw.Draw(image)
       
    # define fonts 
    font_label=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", FONTSIZE_SMALL)
    font_value=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", FONTSIZE_BIG)
   
    # set upper left corner of the working area
    xoffset =  a_x
    yoffset =  a_y
    
    # extract strings from .json records
    label = json_data[0]["label"]
    value = json_data[0]["value"]
    
    # get sizes for text centering 
    value_width, value_height = draw.textsize(value, font = font_value) 
    
    # calculate the position of the left edge of the centered "value"
    x_cent_val = ( epd.width - value_width ) / 2   
    # fill out the quadrant   
    draw.text( (xoffset + BORDER, yoffset) , '%s' %label, fill=BLACK, font=font_label)  
    draw.text( (x_cent_val, yoffset + FONTSIZE + INTERLINE), '%s' %value, fill=BLACK, font=font_value)
    
    #draw a warning sign if status == false
    if json_data[0]["status"] == "false":
        image.paste(warning_sign,( epd.width - sign_width, c_y))
   
    # put the timestamp
    draw.text( (STAMP_OFFSET, h_y), 'Letzte Aktualisierung: {:%d/%m/%Y %H:%M:%S}'.format(datetime.datetime.now()), fill=BLACK)
    
    # display image on the panel
    
    epd.display(image)
    epd.update()