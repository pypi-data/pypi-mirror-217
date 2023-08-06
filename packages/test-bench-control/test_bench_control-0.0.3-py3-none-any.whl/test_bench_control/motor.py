import RPi.GPIO as GPIO
import time
import numpy as np

GPIO.setmode(GPIO.BOARD)

# Raspberry Pi Pin Assignment for TB6600 Driver
DIR = 33
PUL = 35
ENA = 37

DIR_Left = GPIO.HIGH
DIR_Right = GPIO.LOW

ENA_Locked = GPIO.LOW
ENA_Released = GPIO.HIGH

GPIO.setwarnings(False)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

def rotate(degree,slope=0.5,rpm_max=100):
    
    ###########################################################################################
    #  Pre:     degree  (float) - rotation of plate in degrees D=[-inf,inf] 
    #           slope   (float) - how fast motor starts D=[0,1], with 0 = slowest, 1 = fastest
    #           rpm_max (float) - max rpm of motor, NOT the plate! D=[50,300]
    #  Post:    no return value
    #  Example: rotate(degree=-8.6,slope=0.2,rpm_max=200)
    ###########################################################################################

    if degree==0:
        exit()
    if degree<0:
        GPIO.output(DIR, DIR_Left)
    if degree>0:
        GPIO.output(DIR, DIR_Right)
        
    if rpm_max > 300:
        rpm_max = 300
    if rpm_max < 50:
        rpm_max = 50
    if slope > 1:
        slope = 1
    if slope < 0:
        slope = 0
        
    # activate motor and hold torque
    GPIO.output(ENA, ENA_Locked)

    # 1 motor turn equals 400 steps. With i = 1:15, 1 table turn is 15*400 = 6000 steps
    steps=int(abs(degree)*6000/360)
    RPM_of_step = np.zeros(steps)
    slope = 0.8*slope + 0.2 #min slope is 0.2, max slope is 1.0
    rpm_min = 50 #might adapt in future
    steps_until_max_rpm = int((rpm_max-rpm_min)/slope)
    
    # if degree is so small: ramp up and ramp down
    if steps<=2*steps_until_max_rpm:
        #ramp up and down
        for i in range(0,int(steps/2)):
            RPM_of_step[i]=rpm_min+i*slope
            RPM_of_step[steps-i-1]=rpm_min+i*slope
    else:
        #ramp up, stay up and then and down
        for i in range(0,steps_until_max_rpm):
            RPM_of_step[i]=rpm_min+i*slope
            RPM_of_step[steps-i-1]=rpm_min+i*slope
        for i in range(steps_until_max_rpm,(steps-steps_until_max_rpm)):
            RPM_of_step[i]=rpm_max
    
    for i in range(0,len(RPM_of_step)):
        currentfrequency=0.3/(RPM_of_step[i])
        # modulate pulse
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(currentfrequency/2)#(0.0001875)
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(currentfrequency/2)

    # release motor
    GPIO.output(ENA, ENA_Released)