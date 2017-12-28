import RPi.GPIO as GPIO

class Encoder(object):
    def __init__(self, pin_a, pin_b):
        self.ticks = 0
        self.last_change = 0

        self.no_change = 0
        self.a = False
        self.b = False
        self.setup= False
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BOARD)
            
        self.pin_a = pin_a
        self.pin_b = pin_b
        
        pins = [self.pin_a, self.pin_b]
        GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # attach interrupt
        GPIO.add_event_detect(self.pin_a, GPIO.BOTH, callback=self.change)
        GPIO.add_event_detect(self.pin_b, GPIO.BOTH, callback=self.change)
        
    def change(self, channel):
        #a = self.a
        #b = self.b
        if not self.setup:
            self.setup = True
            self.a = GPIO.input(self.pin_a)is GPIO.HIGH
            self.b = GPIO.input(self.pin_b)is GPIO.HIGH
            return

        if(channel == self.pin_a):
            self.a = not self.a
            if self.a is not self.b:
                # Right
                self.ticks += 1
                print("RIGHT")
            else:
                # Left
                self.ticks -= 1
                print("LEFT")
        else:
            self.b = not self.b
            if self.b is self.a:
                # Right
                self.ticks += 1
                print("RIGHT")
            else:
                # Left
                self.ticks -= 1
                print("LEFT")
        print("{},a:{},b:{}".format(self.ticks, self.a, self.b))

    def pin_change(self, channel):
        # print("pin_change {}".format(channel))
        val_a = GPIO.input(self.pin_a)
        val_b = GPIO.input(self.pin_b)
        
        self.a = self.a << 1
        self.a = self.a | val_a
        self.b = self.b << 1
        self.b = self.b | val_b
        
        self.a = self.a & 0b00001111
        self.b = self.b & 0b00001111

        if self.a == 0b00001001 and self.b == 0b00000011:
            self.ticks += 1
        
        if self.a == 0b00000011 and self.b == 0b00001001:
            self.ticks -= 1
        print("pin_change {0} {1} pin_a={2}, pin_b={3}".format(channel, self.ticks, val_a, val_b))

    def read(self):
        return [GPIO.input(self.pin_a), GPIO.input(self.pin_b)]
