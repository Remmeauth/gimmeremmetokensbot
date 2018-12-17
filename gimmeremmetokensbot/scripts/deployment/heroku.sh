#!/usr/bin/env bash

gunicorn app:server -b 0.0.0.0:$PORT
