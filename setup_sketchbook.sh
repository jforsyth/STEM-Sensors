#!/bin/bash
sudo apt install -y git arduino
git clone https://github.com/jforsyth/STEM-Sensors.git

cp -r ~/STEM-Sensors/sketchbook/* ~/Arduino/.
