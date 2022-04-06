# cacof_ryan

Installs
sudo apt-get install pigpio python-pigpio python3-pigpio
sudo apt-get install python3-opencv

Run on start up. Added to start up scrip, run if not Ryan.
sudo pigpiod

Code to add to 'sudo crontab -e'
@reboot sudo pigpiod
@reboot sudo python3 /bin/cv_write_test_multi.py



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

View and convert CPTV to mp4
https://thecacophonyproject.github.io/

sudo cp sweep_stepper.py ../../bin


