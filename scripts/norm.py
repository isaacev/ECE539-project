import sys
import os
import csv
import re

output_dir = sys.argv[1]
input_paths = sys.argv[2:]
if len(sys.argv) < 3:
  print("usage: python norm.py <output directory> [input files ...]")
  sys.exit(1)

def print_row(district):
  cols = [
    district['district'],
    '%d'   % (district['population']),
    '%.5f' % ((district['race_white'] / float(district['population'])) * 100),
    '%.5f' % ((district['race_black'] / float(district['population'])) * 100),
    '%.5f' % ((district['race_native'] / float(district['population'])) * 100),
    '%.5f' % ((district['race_asian'] / float(district['population'])) * 100),
    '%d'   % (district['income_median']),
    '%.5f' % (100.0 - district['at_least_high_school']),
    '%.5f' % (district['at_least_high_school'] - district['at_least_college']),
    '%.5f' % (district['at_least_college']),
  ]
  return ','.join(cols) + '\n'

for input_path in input_paths:
  input_filename = os.path.basename(input_path)
  output_path = os.path.join(output_dir, input_filename)

  with open(input_path, 'r') as input_file:
    with open(output_path, 'w') as output_file:
      reader = csv.reader(input_file)

      state_id = os.path.splitext(os.path.basename(input_path))[0]
      districts = {}
      pattern = r'^District .* Estimate$'

      for rowid, row in enumerate(reader):
        if rowid == 0:
          # get district names and the column that corresponds to that district
          for colid, col in enumerate(row):
            match = re.match(pattern, col)
            if match:
              districts[colid] = {
                'district': state_id + str(len(districts)+1)
              }
        elif rowid == 1:
          # get district population
          for colid, col in enumerate(row):
            if colid in districts:
              districts[colid]['population'] = int(col)
        elif rowid == 2:
          # get district percent white residents
          for colid, col in enumerate(row):
            if colid in districts:
              districts[colid]['race_white'] = int(col)
        elif rowid == 3:
          # get district percent black residents
          for colid, col in enumerate(row):
            if colid in districts:
              districts[colid]['race_black'] = int(col)
        elif rowid == 4:
          # get district percent native american residents
          for colid, col in enumerate(row):
            if colid in districts:
              districts[colid]['race_native'] = int(col)
        elif rowid == 5:
          # get district percent asian residents
          for colid, col in enumerate(row):
            if colid in districts:
              districts[colid]['race_asian'] = int(col)
        elif rowid == 6:
          # get district median income
          for colid, col in enumerate(row):
            if colid in districts:
              districts[colid]['income_median'] = float(col)
        elif rowid == 7:
          # get percent high-school edu. or greater
          for colid, col in enumerate(row):
            if colid in districts:
              districts[colid]['at_least_high_school'] = float(col)
        elif rowid == 8:
          # get percent with college edu. or greater
          for colid, col in enumerate(row):
            if colid in districts:
              districts[colid]['at_least_college'] = float(col)


      for colid in districts:
        output_file.write(print_row(districts[colid]))
      output_file.close()
    input_file.close()
  print(output_path)
