import sys
import traceback

from flask import Flask, request, jsonify

import pandas as pd
import numpy as np
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.INFO)

app = Flask(__name__, static_url_path='')

# input path
path_data = 'data'
path_model = 'models'

# feature definitions
feature_names = ['Day', 'DayOfWeek', 'Hour', 'device']
csv_defaults = [['1'],['1'],['0'],['device_1']]
label_name = ['activated']

dtypes = {'Day': 'category', 'DayOfWeek': 'category', 'Hour': 'category', 'device': 'category', 'activated': 'category'}
df_train = pd.read_csv('data/processed/train.csv', dtype=dtypes)
days = df_train['Day'].unique().tolist()
dows = df_train['DayOfWeek'].unique().tolist()
hours = df_train['Hour'].unique().tolist()
devices = df_train['device'].unique().tolist()

feature_columns = [
    tf.feature_column.embedding_column(
        tf.feature_column.categorical_column_with_vocabulary_list(
            key="Day", 
            vocabulary_list=days),
        7
    ),
    tf.feature_column.embedding_column(
        tf.feature_column.categorical_column_with_vocabulary_list(
            key="DayOfWeek", 
            vocabulary_list=dows),
        5
    ),
    tf.feature_column.embedding_column(
        tf.feature_column.categorical_column_with_vocabulary_list(
            key="Hour", 
            vocabulary_list=hours),
        4
    ),
    tf.feature_column.embedding_column(
        tf.feature_column.categorical_column_with_vocabulary_list(
            key="device", 
            vocabulary_list=devices),
        3
    )
]

# model instantiation, it will restore a previous version of any saved model
classifier = tf.estimator.DNNClassifier(
    feature_columns=feature_columns,
    hidden_units=[128, 32],
    dropout=0.05,
    optimizer=tf.train.FtrlOptimizer(
        learning_rate=0.001,
#         l1_regularization_strength=0.01,
#         l2_regularization_strength=0.001
    ),
    label_vocabulary=['True', 'False'],
    model_dir=path_model
)

# We have our prediction
def input_fn_predict(input):
    def decode_csv(line):
        """Convert a CSV row to a dictonary of features and a label"""
        parsed_line = tf.decode_csv(line, csv_defaults)
        features = parsed_line
        return dict(zip(feature_names, features))

    dataset = (tf.data.TextLineDataset(input)
               .skip(1)  # Skip header row
               .map(decode_csv))
    dataset = dataset.batch(24)
    
    iterator = dataset.make_one_shot_iterator()
    
    return iterator.get_next()    
     
# and associated endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        df = pd.DataFrame()
        df['time'] = pd.date_range(request.json['timestamp'], periods=24, freq='H').ceil('H')
        for i in range(1,7):
            column = "device_"+str(i)
            df[column] = False
        df.set_index(['time'], inplace=True)
        df = df.stack().reset_index()
        df.rename(columns={'level_1': 'device', 0: 'activated'}, inplace=True)
        df['Day'] = df['time'].dt.day
        df['DayOfWeek'] = df['time'].dt.dayofweek
        df['Hour'] = df['time'].dt.hour
        dates = df['time']
        df = df.reindex(columns=feature_names)
        df.to_csv('data/processed/tmp.csv', index=False)

        predictions = classifier.predict(input_fn=lambda: input_fn_predict('data/processed/tmp.csv'))

        result = [] 
        for prediction in predictions:
            result.append(prediction['classes'][0].decode('utf-8'))

        df['time'] = dates
        df['time'].astype('str')
        df['activated'] = result
        df.drop(['Day', 'DayOfWeek', 'Hour'], axis=1, inplace=True)
        df = df.reindex(columns=['time', 'device', 'activated'])
        df.to_csv('data/processed/pred.csv', index=False)

        return df.to_json(orient='index')

    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()})
