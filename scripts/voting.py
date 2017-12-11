import sys
import os
import csv
import re

if len(sys.argv) < 4:
  print("usage: python voting.py <output directory> <voting data> [input files ...]")
  sys.exit(1)

output_dir = sys.argv[1]
voting_path = sys.argv[2]
input_paths = sys.argv[3:]

with open(voting_path, 'r') as voting_file:
  voting_reader = csv.reader(voting_file)
  voting_data = {}
  for rowid, row in enumerate(voting_reader):
    if rowid > 0:
      match = re.match(r'([A-Z]{2})-(..)', row[0])
      if match:
        state = match.group(1)
        distr = match.group(2)
        if distr == 'AL':
          distr = 1
        else:
          distr = int(distr)
        distr = state + str(distr)
        voting_data[distr] = {
          'vote_dem': '%.5f' % float(row[3]),
          'vote_gop': '%.5f' % float(row[4]),
        }
  voting_file.close()

  for input_path in input_paths:
    input_filename = os.path.basename(input_path)
    output_path = os.path.join(output_dir, input_filename)

    with open(input_path, 'r') as input_file:
      reader = csv.reader(input_file)
      with open(output_path, 'w') as output_file:
        writer = csv.writer(output_file)
        for row in reader:
          new_row = row[:]
          distr_data = voting_data[new_row[0]]
          new_row += [distr_data['vote_dem'], distr_data['vote_gop']]
          writer.writerow(new_row)
        output_file.close()
      input_file.close()
