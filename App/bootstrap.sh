#!/bin/bash
debug=True
export FLASK_APP=./src/main.py
flask run -h 0.0.0.0
