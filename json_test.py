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

# This is a simple script to test correctness and test parsing of data from a .json file

import json
import sys
from pprint import pprint

def main(argv):
    
    with open(argv[0]) as data_file:    
        data = json.load(data_file)
        data_file.close()
    
    rec_count = len(data[0]) # number of labels in a record
    print(rec_count)
    print(data[0]["label"]) # display first "label" from the .json file
  
    
    
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))
    main(sys.argv[1:])