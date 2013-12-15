#!/bin/bash
/usr/bin/gunicorn api_server:app -b 127.0.0.1:8000

