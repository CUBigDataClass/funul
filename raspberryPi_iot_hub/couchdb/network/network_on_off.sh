#!/bin/bash

sudo ifconfig wlan0 down
sleep 10
sudo ifconfig wlan0 up
