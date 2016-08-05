#!/bin/bash
# This script installs the 2,7" EPD according to manufactirer's reopsitory on GitHub
# https://github.com/embeddedartists/gratis/tree/master/PlatformWithOS

sudo modprobe spi-bcm2835
cd ./gratis/PlatformWithOS
sudo apt-get install libfuse-dev
sudo COG_VERSION=V2 make rpi-epd_fuse
sudo mkdir /tmp/epd
sudo COG_VERSION=V2 make rpi-epd_fuse
sudo ./driver-common/epd_fuse --panel=2.7 -o allow_other -o default_permissions /tmp/epd
sudo COG_VERSION=V2 make rpi-install
sudo service epd-fuse start
sudo apt-get install python-imaging
