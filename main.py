from gpiozero import LED, Button
from time import sleep

led_pin = 4
print("Working with LED({})".format(led_pin))

led = LED(led_pin)

for i in range(10):
    print("{}".format(i))
    led.on()
    sleep(.1)
    led.off()
    sleep(.1)

