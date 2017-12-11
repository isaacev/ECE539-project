import sys
import os
import csv
import re
import random

if len(sys.argv) != 5:
  print("usage: python regions.py <num regions> <region size> <output file> <input file>")
  sys.exit(1)

num_regions = int(sys.argv[1])
region_size = int(sys.argv[2])
output_path = sys.argv[3]
input_path = sys.argv[4]

def denormalize_district(district):
  # convert percents back into absolute integers
  pop = int(district[1])
  rw  = (float(district[2])  / 100) * pop
  rb  = (float(district[3])  / 100) * pop
  rn  = (float(district[4])  / 100) * pop
  ra  = (float(district[5])  / 100) * pop
  med = int(district[6])
  en  = (float(district[7])  / 100) * pop
  ehs = (float(district[8])  / 100) * pop
  ec  = (float(district[9])  / 100) * pop
  vd  = (float(district[10]) / 100) * pop
  vg  = (float(district[11]) / 100) * pop
  return [district[0], pop, rw, rb, rn, ra, med, en, ehs, ec, vd, vg]

def mean(l):
  return float(sum(l)) / len(l)

def combine_districts(districts):
  districts = [denormalize_district(d) for d in districts]
  pop = sum([int(d[1]) for d in districts])
  return [
    '__',
    pop,
    '%.5f' % ((sum([float(d[2])  for d in districts]) / pop) * 100), # rw
    '%.5f' % ((sum([float(d[3])  for d in districts]) / pop) * 100), # rb
    '%.5f' % ((sum([float(d[4])  for d in districts]) / pop) * 100), # rn
    '%.5f' % ((sum([float(d[5])  for d in districts]) / pop) * 100), # ra
    '%d'   % (mean([int(d[6])    for d in districts])),              # med
    '%.5f' % ((sum([float(d[7])  for d in districts]) / pop) * 100), # en
    '%.5f' % ((sum([float(d[8])  for d in districts]) / pop) * 100), # ehs
    '%.5f' % ((sum([float(d[9])  for d in districts]) / pop) * 100), # ec
    '%.5f' % ((sum([float(d[10]) for d in districts]) / pop) * 100), # vd
    '%.5f' % ((sum([float(d[11]) for d in districts]) / pop) * 100), # vg
  ]

with open(input_path, 'r') as input_file:
  reader = csv.reader(input_file)
  rows = list(reader)
  input_file.close()

  with open(output_path, 'w') as output_file:
    writer = csv.writer(output_file)
    for i in range(0, num_regions):
      r = random.randint(0, len(rows)-1)
      same_state = [x for x in rows if x[0][0:2] == rows[r][0][0:2]]
      chosen = [rows[r]]
      for j in range(0, region_size-1):
        s = random.randint(0, len(same_state)-1)
        chosen += [same_state[s]]
      writer.writerow(combine_districts(chosen))
    output_file.close()
