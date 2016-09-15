#!/bin/bash
cd gratis/PlatformWithOS
sudo COG_VERSION=V2 make rpi-remove
sudo rm -rf /usr/local/lib/python2.7/dist-packages/ea_epd_sensor_values*
sudo rm -rf /usr/local/bin/EPD_*
sudo update-rc.d epd_button remove
sudo rm /etc/init.d/epd_button
