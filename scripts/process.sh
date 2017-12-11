#! /usr/bin/env bash

rm -rf data/{filtered,norm,renamed,voting}
rm -rf data/*.csv

# Data processing pipeline
mkdir -p data/{renamed,filtered,norm,voting}
find data/downloaded -name "*.csv" ! -name "voting.csv"                       \
  | xargs python3 scripts/rename.py data/renamed                              \
  | xargs python3 scripts/filter.py data/filtered                             \
  | xargs python3 scripts/norm.py   data/norm                                 \
  | xargs python3 scripts/voting.py data/voting data/downloaded/voting.csv

# Combine per-state CSV files into a single CSV file
cat data/voting/*.csv > data/districts.csv

# Generate synthetic voting regions
python3 scripts/regions.py 512 2 data/regions2.csv data/districts.csv
python3 scripts/regions.py 256 3 data/regions3.csv data/districts.csv
python3 scripts/regions.py 128 4 data/regions4.csv data/districts.csv
python3 scripts/regions.py 64  5 data/regions5.csv data/districts.csv

# Combine districts and synthetic regions
cat data/*.csv > data/all.csv

# Remove district and region names
cut -d , -f2-12 data/all.csv > data/anon.csv

# Randomly select 100 rows for the testing data
m=100
gshuf data/anon.csv > tmp
head -n $m tmp > data/testing.csv
tail -n +$(( m + 1 )) tmp > data/training.csv
rm tmp
