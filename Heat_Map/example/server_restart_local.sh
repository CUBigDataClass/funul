#!/usr/bin/env bash
sudo kill $(ps aux | grep '[p]ython' | awk '{print $2}') &&
sudo python app_local.py &