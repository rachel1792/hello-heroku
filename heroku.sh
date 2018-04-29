#!/bin/bash
python worker.py --daemon
python clock.py --daemon
gunicorn app:app
