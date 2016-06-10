#!/bin/sh

export APP_CONFIG=dev.cfg
export FLASK_APP=autoapp.py
flask run -h 0.0.0.0 --with-threads
