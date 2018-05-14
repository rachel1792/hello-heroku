#!/bin/bash
python clock.py --daemon
gunicorn app:app
