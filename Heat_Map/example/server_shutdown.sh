#!/usr/bin/env bash
sudo kill $(ps aux | grep '[p]ython' | awk '{print $2}')