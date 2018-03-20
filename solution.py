#!/usr/bin/env python3

"""
This is a sample program for the data science challenge and can be used as a
starting point for a solution.

It will be run as follows;
    sample_solution.py <current time> <input file name> <output file name>

Current time is the current hour and input file is all measured values from
the activation detector in each room for the past few hours.
"""

import numpy as np
import pandas as pd
import sys

def process_input_data(raw_data):
    """It basically does a resampling using the following heuristic:
    For every hour, if an activation occured, then device_activated is one else zero
    """
    pass

def predict_future_activation(current_time, previous_readings):
    """This function predicts future hourly activation given previous sensings.

    It's probably not the best implementation as it just returns a random
    guess.
    """
    # train the model with previous readings
    model = ...

    # Make 24 predictions for each hour starting at the next full hour
    next_24_hours = pd.date_range(current_time, periods=24, freq='H').ceil('H')

    device_names = sorted(previous_readings.device.unique())

    # predict the next 24 hourly
    predictions = model.predict(next_24_hours) #pd.DataFrame(xproduct, columns=['time', 'device'])
    predictions.set_index('time', inplace=True)

    return predictions

if __name__ == '__main__':

    current_time, in_file, out_file = sys.argv[1:]

    previous_readings = pd.read_csv(in_file)
    previous_readings_processed = process_input_data(previous_readings) 
    result = predict_future_activation(current_time, previous_readings)
    result.to_csv(out_file)
