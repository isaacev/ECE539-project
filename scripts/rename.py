'''
Files are downloaded from the US Census website with filenames of the form:
"North_Carolina_All_Districts" This file converts those filenames to the form:
"NC.csv" which is more consistent for later processing.
'''

conv = {
  'Alabama':        'AL',
  'Alaska':         'AK',
  'Arizona':        'AZ',
  'Arkansas':       'AR',
  'California':     'CA',
  'Colorado':       'CO',
  'Connecticut':    'CT',
  'Delaware':       'DE',
  'Florida':        'FL',
  'Georgia':        'GA',
  'Hawaii':         'HI',
  'Idaho':          'ID',
  'Illinois':       'IL',
  'Indiana':        'IN',
  'Iowa':           'IA',
  'Kansas':         'KS',
  'Kentucky':       'KY',
  'Louisiana':      'LA',
  'Maine':          'ME',
  'Maryland':       'MD',
  'Massachusetts':  'MA',
  'Michigan':       'MI',
  'Minnesota':      'MN',
  'Mississippi':    'MS',
  'Missouri':       'MO',
  'Montana':        'MT',
  'Nebraska':       'NE',
  'Nevada':         'NV',
  'New_Hampshire':  'NH',
  'New_Jersey':     'NJ',
  'New_Mexico':     'NM',
  'New_York':       'NY',
  'North_Carolina': 'NC',
  'North_Dakota':   'ND',
  'Ohio':           'OH',
  'Oklahoma':       'OK',
  'Oregon':         'OR',
  'Pennsylvania':   'PA',
  'Rhode_Island':   'RI',
  'South_Carolina': 'SC',
  'South_Dakota':   'SD',
  'Tennessee':      'TN',
  'Texas':          'TX',
  'Utah':           'UT',
  'Vermont':        'VT',
  'Virginia':       'VA',
  'Washington':     'WA',
  'West_Virginia':  'WV',
  'Wisconsin':      'WI',
  'Wyoming':        'WY',
}

import os
import sys
import re
import shutil

output_dir = sys.argv[1]
input_paths = sys.argv[2:]
if len(sys.argv) < 3:
  print("usage: python rename.py <output directory> [input files ...]")
  sys.exit(1)

pattern = r'^(\w+)(_All_Districts|_District_At_Large)\.csv$'
for input_path in input_paths:
  input_filename = os.path.basename(input_path)
  match = re.match(pattern, input_filename)
  if match and conv[match.group(1)]:
    output_path = os.path.join(output_dir, conv[match.group(1)] + '.csv')
    shutil.copyfile(input_path, output_path)
    print(output_path)
