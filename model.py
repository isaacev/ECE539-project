import tensorflow as tf

# describe data structure
NUM_COLS = 9
NUM_INCUMBENTS = 1

CSV_COLUMN_DEFAULTS = [[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]]
CSV_COLUMNS = ['population','race_white','race_black','race_native',
               'race_asian','income_median','edu_nil','edu_high_school',
               'edu_college', 'vote_dem']

NUM_EXAMPLES = {
  'train': 27,
  'validation': 7,
}

def build_model_columns():
  population      = tf.feature_column.numeric_column('population')
  race_white      = tf.feature_column.numeric_column('race_white')
  race_black      = tf.feature_column.numeric_column('race_black')
  race_native     = tf.feature_column.numeric_column('race_native')
  race_asian      = tf.feature_column.numeric_column('race_asian')
  income_median   = tf.feature_column.numeric_column('income_median')
  edu_nil         = tf.feature_column.numeric_column('edu_nil')
  edu_high_school = tf.feature_column.numeric_column('edu_high_school')
  edu_college     = tf.feature_column.numeric_column('edu_college')

  return [
    population,
    race_white,
    race_black,
    race_native,
    race_asian,
    income_median,
    edu_nil,
    edu_high_school,
    edu_college,
  ]

def build_estimator(model_dir):
  cols = build_model_columns()
  return tf.estimator.DNNClassifier(
    model_dir=model_dir,
    feature_columns=cols,
    hidden_units=[3, 3])

def input_fn(data_file, num_epochs, shuffle, batch_size):
  assert tf.gfile.Exists(data_file), (
    '%s not found. Please make sure you have either run data_download.py or '
    'set both arguments --train_data and --test_data.' % data_file)

  def parse_csv(value):
    print('Parsing', data_file)
    columns = tf.decode_csv(value, record_defaults=CSV_COLUMN_DEFAULTS)
    features = dict(zip(CSV_COLUMNS, columns))
    labels = features.pop('vote_dem')
    return features, tf.greater(labels, 50.0)

  # Extract lines from input files using the Dataset API.
  dataset = tf.data.TextLineDataset(data_file)

  # if shuffle:
  #   dataset = dataset.shuffle(buffer_size=NUM_EXAMPLES['train'])

  dataset = dataset.map(parse_csv, num_parallel_calls=5)

  # We call repeat after shuffling, rather than before, to prevent separate
  # epochs from blending together.
  dataset = dataset.repeat(num_epochs)
  dataset = dataset.batch(batch_size)

  iterator = dataset.make_one_shot_iterator()
  features, labels = iterator.get_next()
  return features, labels

def main():
  model_dir = '/Users/isaac/Documents/school/539-project'
  train_data = '/Users/isaac/Documents/school/539-project/FL_train.csv'
  test_data = '/Users/isaac/Documents/school/539-project/FL_test.csv'
  epochs_per_level = 4
  train_epochs = 80
  batch_size = 40

  model = build_estimator(model_dir)

  for n in range(0,4):
    model.train(input_fn=lambda: input_fn(
      train_data, epochs_per_level, True, batch_size))
    results = model.evaluate(input_fn=lambda: input_fn(
      test_data, 1, False, batch_size))
    print('Results as epoch', (n + 1))
    print('-' * 60)
    for key in sorted(results):
      print('%s: %s' % (key, results[key]))

main()
