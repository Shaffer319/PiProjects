#include <iostream>

// wiringpi.com/reference/priority-interrupts-and-therads/
#include <wiringPi.h>

using namespace std;

int led_pin_red = 15;
int led_pin_green = 16;
int encoder_a = 11;
int encoder_b = 13;

int prev_a = 0;
int prev_b = 0;
int invalidTicks = 0;
int noneTicks = 0;
int ticks = 0;

void encoderACallback(void)
{
	int a = digitalRead(encoder_a);
	int b = digitalRead(encoder_b);
	
	if(a == prev_a && b == prev_b){
		noneTicks += 1;
	}
	
	else if (a != prev_a && b != prev_b){
		invalidTicks ++;
	}
	else	
	if(a != prev_a){
		if(a == b){
			ticks --;
		}
		else{
			ticks ++;
		}
	}
	else{
		if(a == b){
			ticks++;
		}else{
			ticks--;
		}
	}
	
	prev_a = a;
	prev_b = b;
}

void encoderBCallback(void)
{

}

void encoderCallback(void)
{
	int a = digitalRead(encoder_a);
	int b = digitalRead(encoder_b);
	
	int c = a << 1 | b;
	int d = prev_a << 1 | prev_b;

	prev_a = a;
	prev_b = b;
	
	if( d == 0b00 and c == 0b10 or
		d == 0b01 and c == 0b00 or
		d == 0b10 and c == 0b11 or
		d == 0b11 and c == 0b01)
	{
		ticks+= 1;
		return;
	}
	
	if( d == 0b00 and c == 0b01 or
		d == 0b01 and c == 0b11 or
		d == 0b10 and c == 0b00 or
		d == 0b11 and c == 0b10){
		ticks -= 1;
		return;
	}
	
	if (d == 0b00 and c == 0b00 or
		d == 0b01 and c == 0b01 or
		d == 0b10 and c == 0b10 or
		d == 0b11 and c == 0b11)
	{          
		noneTicks += 1;
		return;
	}

	if (d == 0b00 and c == 0b11 or 
		d == 0b01 and c == 0b10 or
		d == 0b10 and c == 0b01 or
		d == 0b11 and c == 0b00){
		invalidTicks += 1;
		return;
	}

	cout << "Woops" << endl;
}

int main(void)
{
	cout << "Starting blink" << endl;
	// 15 and 16 are 22 and 23
	// int led_pin_red = 22;
	// int led_pin_green = 23;
	//if(wiringPiSetupGpio() != 0){
	//	return -1;
	//}
	
	// This allows the use of the physical pin numbers
	if(wiringPiSetupPhys() != 0){
		return -1;
	}
	
    pinMode(led_pin_red, OUTPUT);		
    pinMode(led_pin_green, OUTPUT);

    pinMode(encoder_a, INPUT);
    pinMode(encoder_b, INPUT);
    
	pullUpDnControl(encoder_a, PUD_UP);
	pullUpDnControl(encoder_b, PUD_UP);
    
	wiringPiISR(encoder_a, INT_EDGE_BOTH, encoderACallback);
	wiringPiISR(encoder_b, INT_EDGE_BOTH, encoderACallback);
	// wiringPiISR(encoder_a, INT_EDGE_BOTH, encoderCallback);
	// wiringPiISR(encoder_b, INT_EDGE_BOTH, encoderCallback);
    
    for(;;)
    {
		cout << "On" << endl;
        digitalWrite(led_pin_red, HIGH);
        digitalWrite(led_pin_green, LOW);
        delay(500);
        cout << "Off" << endl;
        digitalWrite(led_pin_red, LOW);
        digitalWrite(led_pin_green, HIGH);
        delay(500);
        cout<< "Ticks " << ticks << " None" << noneTicks << " Invalid " <<invalidTicks << endl;
    }
    
    
    
    return 0;
}
