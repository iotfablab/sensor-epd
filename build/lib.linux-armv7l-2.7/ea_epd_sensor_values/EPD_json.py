import sys
import json
import os
from EPD import EPD
from EPD_display_values import EPD_display_values
from EPD_display_img import EPD_display_img
from EPD_ip import EPD_ip

def main( argv ):

    DIR = os.path.abspath(os.path.dirname(__file__))
    
    epd = EPD()
  
    if len(argv) == 0:
        epd.clear()
        epd.clear() # Doubled clear to avoid ghosting
        
    elif argv[0] == 'biba':
        EPD_display_img(epd, DIR + '/Images/biba_logo.xbm')
        
    elif argv[0] == 'bibaqr':
        EPD_display_img(epd, DIR + '/Images/biba_qr.xbm')
        
    elif argv[0] == 'test1':
        json_file = open(DIR + '/json_dummies/json_input_1.json', 'r')
        json_data = json.load(json_file)
        json_file.close()        
        EPD_display_values(epd, json_data)      
    elif argv[0] == 'test2':
        json_file = open(DIR + '/json_dummies/json_input_2.json', 'r')
        json_data = json.load(json_file)
        json_file.close()        
        EPD_display_values(epd, json_data)      
    elif argv[0] == 'test3':
        json_file = open(DIR + '/json_dummies/json_input_3.json', 'r')
        json_data = json.load(json_file)
        json_file.close()        
        EPD_display_values(epd, json_data)      
    elif argv[0] == 'test4':
        json_file = open(DIR + '/json_dummies/json_input_4.json', 'r')
        json_data = json.load(json_file)
        json_file.close()        
        EPD_display_values(epd, json_data)    
    elif argv[0] == 'ip':
        EPD_ip(epd)      
        
    else:
        json_file = open(argv[0], 'r')
        json_data = json.load(json_file)
        json_file.close()        
        EPD_display_values(epd, json_data)       
# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))
    main(sys.argv[1:])
