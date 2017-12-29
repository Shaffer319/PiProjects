#include <stdio.h>
#include <wiringPi.h>

int led_pin_red = 22;
int led_pin_green = 23;
int main(void)
{
	printf("Starting blink\r\n");
	
	if(wiringPiSetupGpio() == -1)
		return -1;
		
    pinMode(led_pin_red, OUTPUT);
		
    pinMode(led_pin_green, OUTPUT);
    
    for(;;)
    {
		printf("On\r\n");
        digitalWrite(led_pin_red, HIGH);
        digitalWrite(led_pin_green, LOW);
        delay(500);
        printf("Off\r\n");
        digitalWrite(led_pin_red, LOW);
        digitalWrite(led_pin_green, HIGH);
        delay(500);
    }
    
    return 0;
}
