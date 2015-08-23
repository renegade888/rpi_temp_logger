!#/usr/bin/env bash 
sudo apt-get update
sudo apt-get intsall apache2
sudo apt-get install sqlite3 -y
sudo mkdir /var/www/tmplog
sudo a2enmod mpm_prefork cgi
sudo cp ~/rpi_temp_logger/tempdb2.db /var/www/tmplog
sudo chown www-data:www-data /var/www/tmplog/tempdb2.db
sudo ln -s ~/rpi_temp_logger/monitor.py /usr/lib/cgi-bin/
sudo chown www-data:www-data /usr/lib/cgi-bin/monitor.py
sudo ln -s ~/rpi_temp_logger/webgui.py /var/www/tmplog/index.py
