#!/bin/bash

gunicorn -c /app/gunicorn.config.py main:app
