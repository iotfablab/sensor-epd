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
