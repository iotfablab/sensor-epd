from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import datetime
import os


WHITE = 1
BLACK = 0
FONTSIZE_SMALL = 14
FONTSIZE_BIG = 45
FONTSIZE_STAMP = 15
INTERLINE = 10
BORDER  = 3
STAMPSTRIPE = 15
STAMP_OFFSET = 65
DIR = os.path.abspath(os.path.dirname(__file__))

def EPD_display_values(epd, json_data):

# define characteristic points of EPD

# One record
#_________________________________________
#|a ----->X           b                 c|
#| Y|                                    |
#|  |                                    |
#|  V          field '0'                 |
#|                                       |
#|d                   e                 f|
#|                                       |
#|                                       |
#|                                       |
#|____________________h__________________|
#|g             STAMPSTRIPE             i|
#|j_____________________________________k|

# Two records
#_________________________________________
#|a ----->X           b                 c|
#| Y|                                    |
#|  |            field '0'               |
#|  V                                    |
#|_______________________________________|
#|d                   e                 f|
#|                                       |
#|               field '1'               |
#|                                       |
#|____________________h__________________|
#|g             STAMPSTRIPE             i|
#|j_____________________________________k|

# Three records
#_________________________________________
#|a ----->X          |b                 c|
#| Y|                |                   |
#|  |   field[0,0]   |     field[0,1]    |
#|  V                |                   |
#|___________________|__________________ |
#|d                   e                 f|
#|                                       |
#|                field[1,0]             |
#|                                       |
#|____________________h__________________|
#|g             STAMPSTRIPE             i|
#|j_____________________________________k|

# Four records
#_________________________________________
#|a ----->X          |b                 c|
#| Y|                |                   |
#|  |   field[0,0]   |     field[0,1]    |
#|  V                |                   |
#|___________________|__________________ |
#|d                  |e                 f|
#|                   |                   |
#|     field[1,0]    |     field[1,1]    |
#|                   |                   |
#|___________________|h__________________|
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
    font_label=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", FONTSIZE_SMALL)
    font_value=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", FONTSIZE_BIG)
    font_stamp=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", FONTSIZE_STAMP)
        
    # initially set all white image and image in the background
    image = Image.new('1', epd.size, WHITE)
    warning_sign = Image.open( DIR + '/Images/warning_28x28.xbm', 'r')
    sign_width, sign_height = warning_sign.size

    # prepare for drawing
    draw = ImageDraw.Draw(image)
  
    # number of records in .json file
    rec_count = len(json_data)
    
    #draw stampstripe line
    draw.line( [ ( g_x, g_y ),( i_x, i_y ) ], fill=BLACK)
       
    # draw fields borders
    if rec_count == 2:
        # draw a vertical line throung the middle
        draw.line( [ ( d_x, d_y ),( f_x, f_y ) ], fill=BLACK)
    if rec_count == 3:
        # draw borders
        draw.line( [ ( b_x, b_y ),( e_x, e_y ) ], fill=BLACK)
        draw.line( [ ( d_x, d_y ),( f_x, f_y ) ], fill=BLACK)
    if rec_count == 4:
        # draw quadrant borders
        draw.line( [ ( b_x, b_y ),( h_x, h_y ) ], fill=BLACK)
        draw.line( [ ( d_x, d_y ),( f_x, f_y ) ], fill=BLACK)        
        
    # encode the fields into binary values
    if rec_count == 1:
        list_of_fields =[ 0 ]
    if rec_count == 2:
        list_of_fields =[ 0, 1 ]
    if rec_count == 3:
        list_of_fields=[ [0, 0], [0, 1], [1, 0] ]
    if rec_count == 4:
        list_of_fields=[ [0, 0], [0, 1], [1, 0], [1, 1] ]
        
        
    for field in list_of_fields:
        
    #decode the binary value into ident
        if rec_count == 1:
            ident = field # only 0
        if rec_count == 2:
            ident = field # 0 or 1
        if rec_count == 3:
            ident = field[1]*1 + field[0]*2 # 0, 1 or 2 
        if rec_count == 4:
            ident = field[1]*1 + field[0]*2 # 0, 1, 2 or 3
            
    # extract strings from .json records
        label = json_data[ident]["label"]
        value = json_data[ident]["value"]
    # get sizes for text centering 
        value_width, value_height = draw.textsize(value, font = font_value)

    # set upper left corner of the current field
        if rec_count == 1:        
            xoffset = 0
            yoffset = 0
        if rec_count == 2:
            xoffset = 0
            yoffset = field * d_y
        if rec_count == 3:
            xoffset = field[1] * e_x
            yoffset = field[0] * e_y
        if rec_count == 4:
            xoffset = field[1] * e_x
            yoffset = field[0] * e_y

    
    # calculate the position of the left top corner of the centered "value"
        if rec_count == 1:
            y_cent_val = ( epd.height - 1.2*value_height - sign_height - 2*BORDER) / 2 + sign_height + BORDER
            x_cent_val = ( epd.width - value_width) / 2
            
        if rec_count == 2:
            y_cent_val = yoffset + ( epd.height / 2 - 1.2*value_height - sign_height - 2*BORDER) / 2 + sign_height + BORDER
            x_cent_val = ( epd.width - value_width) / 2
            
        if rec_count == 3:
            y_cent_val = yoffset + ( epd.height / 2 - 1.2*value_height - sign_height - 2*BORDER) / 2 + sign_height + BORDER
            if field == [0, 0] or field == [0, 1]:
                x_cent_val = xoffset + ( epd.width / 2 - value_width ) / 2    
            elif field == [1, 0]:
                x_cent_val = ( epd.width - value_width ) / 2    
                
        if rec_count == 4:
            y_cent_val = yoffset + ( epd.height / 2 - 1.2*value_height - sign_height - 2*BORDER) / 2 + sign_height + BORDER
            x_cent_val = xoffset + ( epd.width / 2 - value_width ) / 2  
            
    
    # fill out the fields                    
        draw.text( (xoffset + BORDER, yoffset + BORDER) , '%s' %label, fill=BLACK, font=font_label)  
        draw.text( (x_cent_val, y_cent_val), '%s' %value, fill=BLACK, font=font_value)
        
    #draw a warning sign if the connection status is "false"
        if json_data[ident]["status"] == "false":
            if rec_count == 1:
                image.paste(warning_sign,( c_x - sign_width - BORDER, c_y + BORDER))
                
            elif rec_count == 2:
                image.paste(warning_sign,( c_x - sign_width - BORDER, yoffset + BORDER))
                
            elif rec_count == 3:
                if ident == 0 or ident == 1:
                    image.paste(warning_sign,( b_x + xoffset - sign_width - BORDER, BORDER))  
                elif ident == 2:
                    image.paste(warning_sign,( c_x - sign_width - BORDER, f_y + BORDER))
                    
            elif rec_count == 4:
                image.paste(warning_sign,( e_x - sign_width + xoffset - BORDER, yoffset + BORDER))  
                              
    # put the timestamp
    draw.text( (STAMP_OFFSET, h_y), '{:%d/%m/%Y %H:%M:%S}'.format(datetime.datetime.now()), fill=BLACK, font = font_stamp)
    
    # display image on the panel
    epd.display(image)
    epd.update()
        
        