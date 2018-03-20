# WattX-Data-Science-Challenge

## Introduction

To solve the test proposed, I will use:

- python >= 3.5
- virtualenv
- Jupyter notebook
- numpy / pandas / matplotlib / seaborn
- scikit-learn and TensorFlow
- flask
- Docker

## Setup

Clone the following repository: `https://github.com/MeTaNoV/WattX-Data-Science-Challenge.git`

```bash
cd /some/path/WattX-Data-Science-Challenge
```

Setup the environment by using virtualenv:

```bash
virtualenv venv
```

Then activate the environment:

```bash
source venv/bin/activate (or source venv/Scripts/activate on windows)
```

And install the required package: (choose the proper requirements file w/ or w/o GPU, depending on your HW)

```bash
pip install -r requirement-gpu.txt
```

## Approach

We will conduct our experiment in two phases using Jupyter Notebooks.

The first will take care of data analysis and preparation.
The second will focus on model design and prediction.

Then, we will build a small Flask server for the model to be called for predictions.

```bash
jupyter notebook
```

### Data Analysis and Preparation

Open the notebook named `Data - Analysis Cleaning Preparation.ipynb` and follow the instructions from there.

### Model Design and Prediction

Open the notebook named `Model - Design Prediction.ipynb` and follow the instructions from there.

### Model Serving

Now that we finalized our model, we need to be able to serve it. We will use a simple flask application to perform this task.

The code for the server application can be found in `ml_server.py`.

It basically creates a server with one endpoints. I slightly adapted the code from the notebook.

To launch the server, simply execute the following:

```bash
./run_server.sh
```

The server could be quickly tested by running the prediction or training scripts in another console:

```bash
./run_prediction.sh > result.json
```

## Conclusion

We can see that with a rather low effort in feature engineering and model design, we managed to have a model that performed
rather well with an accuracy of 91% and an AUC-ROC of 0.95.

Here is a list of actions which could increase our performance:

- acquire more data to increase overall performance but also enables a wider range of seasonnality predictions (monthly, yearly).
- add external data like holidays which can have impact if this is a professional building affected by such day.
- instead, use a time series model like LSTM optionally completed by a convolutional layer to maximize the time series effect.
- do more fine parameter tuning