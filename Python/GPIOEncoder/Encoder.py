import RPi.GPIO as GPIO

class Encoder(object):
    def __init__(self, pin_a, pin_b):
    
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BOARD)
            
        self.pin_a = pin_a
        self.pin_b = pin_b

        pins = [self.pin_a, self.pin_b]
        GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def read(self):
        return [GPIO.input(self.pin_a), GPIO.input(self.pin_b)]
