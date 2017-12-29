import RPi.GPIO as GPIO
from Encoder import Encoder
import time


def main():
    print("Entering GPIOEncoder/__main__.py:")
    
    try :
        GPIO.setmode(GPIO.BOARD) 
        
        GPIO.setup(15, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        encoder = Encoder(11,13)
        # GPIO.setup([15,16], GPIO.OUT)
        while(True):
            print("Ticks:{}, None Bounces{}, Invalids{}".format(encoder.ticks, encoder.noneTicks, encoder.invalidTicks))
            time.sleep(0.1)
        # for i in range(0, 10):
        #    time.sleep(1)
        for i in range(0, 1000): #while(True):
            value = encoder.read()
            GPIO.output(15, value[0])
            GPIO.output(16, value[1])
            time.sleep(.01)
        
    except KeyboardInterrupt:
        GPIO.cleanup()
    GPIO.cleanup()
    print("Exiting GPIOEncoder/__main__.py")
if __name__ == "__main__":
    main()
