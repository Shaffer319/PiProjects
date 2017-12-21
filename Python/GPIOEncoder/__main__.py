import RPi.GPIO as GPIO
from Encoder import Encoder
import time


def main():
    print("GPIOEncoder/__main__.py is running main()")
    GPIO.setmode(GPIO.BOARD) 
    
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    encoder = Encoder(11,13)
    # GPIO.setup([15,16], GPIO.OUT)
    
    # for i in range(0, 10):
    #    time.sleep(1)
    for i in range(0, 1000): #while(True):
        value = encoder.read()
        GPIO.output(15, value[0])
        GPIO.output(16, value[1])
        time.sleep(.01)
   
    GPIO.cleanup()

if __name__ == "__main__":
    main()
