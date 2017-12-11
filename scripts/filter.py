'''
Each CSV file contains a lot of data about a state's districts. Most of that
data is not relevant to this project and the lines of data that are relevant
are the same line numbers in each file so this script removes any lines that
aren't known to be necessary.
'''

needed = [
  0,   # column names
  1,   # total population
  22,  # race (white)
  23,  # race (black)
  24,  # race (native)
  25,  # race (asian)
  199, # median income
  240, # edu (high school or greater)
  241, # edu (college or greater)
]

import sys
import os

output_dir = sys.argv[1]
input_paths = sys.argv[2:]
if len(sys.argv) < 3:
  print("usage: python filter.py <output directory> [input files ...]")
  sys.exit(1)

for input_path in input_paths:
  input_filename = os.path.basename(input_path)
  output_path = os.path.join(output_dir, input_filename)
  contents = ''

  with open(input_path, 'r') as input_file:
    lines = input_file.read().split("\n")
    input_file.close()
    filtered = [lines[i] for i in needed]
    contents = "\n".join(filtered)
  with open(output_path, 'w') as output_file:
    output_file.write(contents)
    output_file.close()
    print(output_path)
