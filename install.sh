!#/usr/bin/env bash 
#Sudo access
sudo -v 
sudo apt-get update
sudo apt-get intsall apache2 -y
sudo apt-get install sqlite3 -y
sudo a2enmod mpm_prefork cgi
sudo mkdir -p /var/www/tmplog
cat ~/rpi_temp_logger/createDatabase.sql | sqlite3 tempdb2.db

if [ -e /var/www/tmplog/tempdb2.db ]; then
    sudo mv /var/www/tmplog ~/tempdb2.bak
fi
sudo mv  ~/rpi_temp_logger/tempdb2.db /var/www/tmplog
sudo ln -s ~/rpi_temp_logger/monitor.py /usr/lib/cgi-bin/
sudo ln -s ~/rpi_temp_logger/webgui.py /var/www/tmplog/index.py

sudo chown www-data:www-data /usr/lib/cgi-bin/monitor.py
sudo chown www-data:www-data /var/www/tmplog/tempdb2.db
