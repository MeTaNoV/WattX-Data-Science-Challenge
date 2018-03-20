#!/bin/bash

# POST method predict
curl -d '{
    "timestamp": "2016-09-01 00:00:00"
}' -H "Content-Type: application/json" \
   -X POST http://localhost:5000/predict
