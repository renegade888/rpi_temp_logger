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
sudo cp ~/rpi_temp_logger/tmplog.conf /etc/apache2/sites-enabled
sudo mv  ~/rpi_temp_logger/tempdb2.db /var/www/tmplog
sudo ln -s ~/rpi_temp_logger/monitor.py /usr/lib/cgi-bin/
sudo ln -s ~/rpi_temp_logger/webgui.py /var/www/tmplog/index.py

sudo chown www-data:www-data /usr/lib/cgi-bin/monitor.py
sudo chown www-data:www-data /var/www/tmplog/tempdb2.db
#Add Crontab to get data from sensors
sudo -l > currentCron
sudo echo "* * * * * /usr/lib/cgi-bin/monitor.py" >> currentCron
sudo crontab currentCron && sudo rm currentCron
#enable GPIO
sudo echo "dtoverlay=w1-gpio" >> /boot/config.txt
#restart to enable GPIO
sudo reboot now
