# cacof_ryan

Installs
sudo apt-get install pigpio python-pigpio python3-pigpio
sudo apt-get install python3-opencv

Methods
https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-rtc-time

Run on start up. Added to start up scrip, run if not added to crontab as below
sudo pigpiod

Code to add to 'sudo crontab -e' for startup scripts
@reboot sudo pigpiod
@reboot sudo python3 /bin/cv_write_test_multi.py
@reboot sudo python3 /bin/sweep_stepper.py


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

Copying commands
Program to bin
sudo cp sweep_stepper.py ../../../../../bin
Videos to USB
sudo cp static_comp_IR_2022* ../../../../../media/usb/video
20220410.214721.645062.cptv

Empty folder
sudo rm *
sudo rm static_comp_IR_2022-06-22_23*
trash-empty

Create USB mount point
ls -l /dev/disk/by-uuid/
sudo mkdir /media/usb
sudo chown -R pi2:pi2 /media/usb

Mount USB
sudo mount /dev/sda1 /media/usb -o uid=pi2,gid=pi2
Unmount USB
sudo umount /media/usb












