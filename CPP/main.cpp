#include <wiringPi.h>
int led_pin = 22;
int main(void)
{
    wiringPiSetup();
    pinMode(led_pin, OUTPUT);
    
    for(;;)
    {
        digitalWrite(led_pin, HIGH);
        delay(500);
    
        digitalWrite(led_pin, LOW);
        delay(500);
    }
    
    return 0;
}