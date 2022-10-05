#!/bin/sh
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=0
flask run --host=0.0.0.0