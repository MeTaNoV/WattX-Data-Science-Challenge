# Interview challenge - WATTx Data Science candidates

The challenge consists of two parts - the first is the main challenge, the second is a bonus task.

## 1) Occupancy prediction model

### Challenge Description

You are provided with time series data from motion sensors (in this case [passive infrared sensors](https://en.wikipedia.org/wiki/Passive_infrared_sensor)). These sensors can be installed in buildings to help determine occupancy of rooms or movement in corridors. The data from these devices can be used to turn lights on and off or to derive optimized heating or ventilation schedules. Judging from the readings, you might know that nobody is usually in the office at a certain time of day so you can turn of the ventilation at this time.

In our case, sensors were installed in 7 different meeting rooms of an office building and recorded occupancy values in these rooms for two months (July and August 2016). Your objective is to write a *model* which can *predict occupancy for the next 24h after a given timestamp*. The input for the predictor are all sensor readings up to the given timestamp. The output should be a value of 1 if you predict that the room will be occupied and 0 if you predict that it will not be occupied for each of the following 24 hours. You evaluate your predictor based on a score that compares the predicted states with the actual states in the test set.

Are there any points you could think of that could help improve your result (e.g. what if you had more data)?

### Submission details

You should create a program that takes 3 arguments like this:

    ./sample_solution.py <timestamp> <input file csv> <output file csv>

* `timestamp` Is the input time. Your predictions should begin in the hour following this timestamp.
* `input file` The history of all sensor readings up to the input time. See format in `data/device_activations.csv`. The sensors in the different rooms are called 'device_[1-7]'.
* `output file` This is where you write your results to. See format in `data/sample_solution.csv`

### Dummy solution

To help make input / output easy to understand we have included a dummy solution as well as some sample data. If you run it as follows

    ./sample_solution.py '2016-08-31 23:59:59' data/device_activations.csv myresult.csv

Then you should get the file `data/sample_solutions.csv`.

## 2) Bonus: Dockerized REST API

Now that you have a model that serves predictions, build a simple Python application that predicts the occupancy of one or several rooms for the next 24 hours!

This task consists in *writing a simple REST API* with a single endpoint (GET or POST) that returns those predictions for the next 24 hours as JSON. Ideally, use Docker to containerize your API.

Example usage of your Docker application:

    docker build -t <your-rest-api-docker-image> .
    docker run -t <your-rest-api-docker-image> -d
    curl http://<DOCKER-IP>:5000/predict

## Evaluation

Your challenge results will be evaluated based on the following criteria

* prediction accuracy (for the first part)
* code cleanliness and documentation
* level of creativity / ingenuity of your solution

## Questions

Feel free to [email us](mailto:ds@wattx.io) with any questions you might have about the challenge.

Looking forward to your submission!
