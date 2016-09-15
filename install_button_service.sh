sudo cp ea_epd_sensor_values/bin/EPD_button  /usr/local/bin/
sudo chmod 755 /usr/local/bin/EPD_button
sudo cp ea_epd_sensor_values/daemon/epd_button /etc/init.d
sudo chmod 755 /etc/init.d/epd_button
sudo update-rc.d epd_button defaults
