!#/usr/bin/env bash 

sudo apt-get update
sudo apt-get intsall apache2
sudo apt-get install sqlite3 -y
sudo mkdir /var/www/tmplog
sudo a2enmod mpm_prefork cgi

#--Add:/etc/apache2/sites-enabled/000-default
#    <Directory /var/www/tmplog
#        Options +ExecCGI
#        DirectoryIndex index.py
#    </Directory>
#    AddHandler cgi-script .py
#    DocumentRoot /var/www/tmplog

sudo cp tempdb2.db /var/www/tmplog
sudo chown www-data:www-data /var/www/tmplog/tempdb2.db
git clone https://github.com/poohzrn/rpi_temp_logger
sudo ln -s ~/rpi_temp_logger/monitor.py /usr/lib/cgi-bin/
sudo chown www-data:www-data /usr/lib/cgi-bin/monitor.py
sudo ln -s ~/rpi_temp_logger/webgui.py /var/www/tmplog/index.py
#/boot/config.txt -> dtoverlay=w1-gpio
