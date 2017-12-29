import RPi.GPIO as GPIO
"""
 class GPIO(object):
    HIGH = 1
    LOW = 0
    IN = 0
    OUT = 1
    INOUT = 2
    PUD_UP = 1
    BOTH = 2
    BOARD = 1
    @staticmethod
    def input(pin):
        return GPIO.HIGH
    @staticmethod
    def setup(pins, mode, pull_up_down=PUD_UP):
        pass
    @staticmethod
    def setmode(value):
        pass
    @staticmethod
    def getmode():
        return None
    @staticmethod
    def add_event_detect(pin, mode, callback):
        pass
""" 
class Encoder(object):
    def __init__(self, pin_a, pin_b):
        self.ticks = 0
        
        self.last_change = 0
        self.noneTicks = 0
        self.invalidTicks = 0
        self.no_change = 0
        self.a = 0
        self.b = 0
        
        self.setup= False
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BOARD)
            
        self.pin_a = pin_a
        self.pin_b = pin_b
        
        pins = [self.pin_a, self.pin_b]
        GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # attach interrupt
        GPIO.add_event_detect(self.pin_a, GPIO.BOTH, callback=self.change_and_poll)
        GPIO.add_event_detect(self.pin_b, GPIO.BOTH, callback=self.change_and_poll)
        
    def change(self, channel):
        # Seems to work in test but on on pi
        #a = self.a
        #b = self.b
        if not self.setup:
            self.setup = True
            self.a = GPIO.input(self.pin_a)
            self.b = GPIO.input(self.pin_b)
            return

        if(channel == self.pin_a):
            self.a = not self.a
            if self.a is not self.b:
                # Right
                self.ticks += 1
                # print("RIGHT")
            else:
                # Left
                self.ticks -= 1
                # print("LEFT")
        else:
            self.b = not self.b
            if self.b is self.a:
                # Right
                self.ticks += 1
                # print("RIGHT")
            else:
                # Left
                self.ticks -= 1
                # print("LEFT")
        # print("{},a:{},b:{}".format(self.ticks, self.a, self.b))
        self.noneTicks +=1

    def change_and_poll(self, channel):
        a = GPIO.input(self.pin_a)
        b = GPIO.input(self.pin_b)
        
        c = a << 1 | b
        d = self.a << 1 | self.b
        self.a = a
        self.b = b
        if d == 0b00 and c == 0b11 or \
            d == 0b01 and c == 0b10 or\
            d == 0b10 and c == 0b01 or \
            d == 0b11 and c == 0b00:
            self.invalidTicks += 1
            # print("Invalid state change: prev{}, cur{} ".format(d, c))
            return;
            
        if d == 0b00 and c == 0b10 or \
            d == 0b01 and c == 0b00 or\
            d == 0b10 and c == 0b11 or \
            d == 0b11 and c == 0b01:
            self.ticks+= 1
            # print("Right")
            return;
            
        if d == 0b00 and c == 0b01 or \
            d == 0b01 and c == 0b11 or\
            d == 0b10 and c == 0b00 or \
            d == 0b11 and c == 0b10:
            self.ticks -= 1
            # print("Left")
            return;
            
        if d == 0b00 and c == 0b00 or \
            d == 0b01 and c == 0b01 or\
            d == 0b10 and c == 0b10 or \
            d == 0b11 and c == 0b11:            
            self.noneTicks += 1
            # print("None")
            return;

        # If a cases is not handled    
        print("Woops")
        
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
