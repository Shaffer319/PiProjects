import RPi.GPIO as GPIO

class Encoder(object):
    def __init__(self, pin_a, pin_b):
        self.ticks = 0
            
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BOARD)
            
        self.pin_a = pin_a
        self.pin_b = pin_b
        
        pins = [self.pin_a, self.pin_b]
        GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # attach interrupt
        GPIO.add_event_detect(self.pin_a, GPIO.CHANGE, callback=self.pin_a_change, bouncetime=1)
        GPIO.add_event_detect(self.pin_b, GPIO.CHANGE, callback=self.pin_b_change, bouncetime=1)
        
    def pin_a_change(self):
        print("pin_a_change")
        pass
        
    def pin_b_change(self):
        print("pin_b_change")
        pass
        
    def read(self):
        return [GPIO.input(self.pin_a), GPIO.input(self.pin_b)]
