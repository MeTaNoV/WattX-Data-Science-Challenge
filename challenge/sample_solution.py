#!/usr/bin/env python3

"""
This is a sample program for the data science challenge and can be used as a
starting point for a solution.

It will be run as follows;
    sample_solution.py <current time> <input file name> <output file name>

Current time is the current hour and input file is all measured values from
the activation detector in each room for the past few hours.
"""


import itertools
import numpy as np
import pandas as pd
import sys


def predict_future_activation(current_time, previous_readings):
    """This function predicts future hourly activation given previous sensings.

    It's probably not the best implementation as it just returns a random
    guess.
    """
    # make predictable
    np.random.seed(len(previous_readings))

    # Make 24 predictions for each hour starting at the next full hour
    next_24_hours = pd.date_range(current_time, periods=24, freq='H').ceil('H')

    device_names = sorted(previous_readings.device.unique())

    # produce 24 hourly slots per device:
    xproduct = list(itertools.product(next_24_hours, device_names))
    predictions = pd.DataFrame(xproduct, columns=['time', 'device'])
    predictions.set_index('time', inplace=True)

    # Random guess!
    predictions['activation_predicted'] = np.random.randint(2, size=len(predictions))
    return predictions


if __name__ == '__main__':

    current_time, in_file, out_file = sys.argv[1:]

    previous_readings = pd.read_csv(in_file)
    result = predict_future_activation(current_time, previous_readings)
    result.to_csv(out_file)
