_____________________________________________________________________________
Package for controlling our test bench with:

- Raspberry Pi 4B (Raspberry Pi OS 64-bit) 
- Nema 23 stepper motor with TB6600 Driver
- 2 IMX477 Raspberry Pi Cameras and Arducam 4x Multiplexer V2.2
_____________________________________________________________________________
How to install and setup:

- pip install test_bench_control
- in config.txt change 'camera_auto_detect=1' to 'camera_auto_detect=0'
- in config.txt add 'dtoverlay=camera-mux-4port,cam0-imx477,cam1-imx477'
_____________________________________________________________________________
How to use:

from test_bench_control import camera,motor

motor.rotate(degree=-8.6,slope=0.2,rpm_max=200)
camera.take_picture(0,"road/to/pic","my_pic.jpg")
 