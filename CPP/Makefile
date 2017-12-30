
bin/blink: main.o
	g++ main.o -o bin/blink -lwiringPi
    
main.o: main.cpp
	g++ -c main.cpp -lwiringPi
    
clean:
	rm -r bin/
	rm *.o
