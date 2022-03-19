# cacof_ryan

Installs
sudo pip3 install adafruit-circuitpython-motorkit
sudo apt-get install pigpio python-pigpio python3-pigpio
sudo apt-get install python3-opencv

Run on start up. Added to start up scrip, run if not Ryan.
sudo pigpiod


Restart camera AI software
sudo systemctl restart classifier.service


Mac SSH commands
sudo ssh pi2@promptlygladbuffalo-new.local

Internet camera page
On Mac
http://promptlygladbuffalo-new.local/

On RPI
localhost.local


Update permissions for all files
sudo chmod -R u=rwx,g=wrx,o=rwx cacof_ryan/

