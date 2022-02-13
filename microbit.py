# Sample of the code used in the microbit
from microbit import *

threshold = 100
FPS = 120

while True:
    # Get and return the accelerometer values
    gyroX = accelerometer.get_x()
    gyroY = accelerometer.get_y()
    print(gyroX, gyroY)
    
    # display the direction 
    if(gyroX > threshold):
        display.show('R')
        
    elif(gyroX < threshold * -1):
        display.show('L')
        
    elif(gyroY > threshold):
        display.show('B')
        
    elif(gyroY < threshold * -1):
        display.show('F')
        
    else:
        display.show('-')
    
    sleep(1000/FPS)