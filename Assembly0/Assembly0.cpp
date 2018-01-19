#include "cknetserial.h"
#include <boost/asio.hpp>
#include <iostream>
#include <cmath>
#include <cstdio>

int bauds = 57600;

CKNetSerial serial("/dev/ttyUSB0", serial_port_base::baud_rate(bauds));

void
hnd1(int sig)
{
	serial.setSpeed(0, 0);//stop
	serial.setPositionCounter(0, 0);
	std::cout << std::endl << "interrupted" << std::endl;
	fflush(stdout);
	exit(0);
}

int
main(int argc, char **argv) {
	signal(SIGINT, hnd1);
	char c;
	int sign = 1, times = 1;
	float mot1 = 50, mot2 = 50, angle = asin(1.0);
	std::cout << "enter\n'+' to start work\nelse character to set configs" << std::endl;
	fflush(stdout);
	std::cin >> c;
	fflush(stdin);
	if (c != '+') {
		std::cout << "settings mode\nenter\n'b' to change bauds\n't' to change waiting limit\n";
		std::cout << "'s' to change motors speeds\n'a' to change rotation angle\n";
		std::cout << "'r' to create new terminal\nelse character to exit settings mode\n";
		fflush(stdout);
		while (c != '+') {
			std::cin >> c;
			fflush(stdin);
			switch (c)
			{
				default :	std::cout << "settings saved" << std::endl;
							fflush(stdout);
							c = '+';
							break;
				case 'b':	std::cin >> bauds;
							fflush(stdin);
							break;
				case 't':	std::cin >> times;
							fflush(stdin);
							break;
				case 's':	std::cin >> mot1 >> mot2;
							fflush(stdin);
							break;
				case 'a':	std::cin >> angle;
							fflush(stdin);
							break;
				case 'r':	CKNetSerial serial("/dev/ttyUSB0", serial_port_base::baud_rate(bauds));
							break;
			}
		}
	}
	std::cout << "control mode\nenter\n'w' to move forward\n'a' to move left\n's' to move back\n";
	std::cout << "'d' to move right\n'q' to stop\n'-' or else character to finish work\n";
	fflush(stdout);
	while (1) {
		std::cin >> c;
		fflush(stdin);
		switch (c)
		{
			default :	std::cout << "exited" << std::endl;
						fflush(stdout);
			case '-':	serial.setSpeed(0, 0);//stop
						serial.setPositionCounter(0, 0);
						return 0;
			case 'q':	serial.setPositionCounter(0, 0);
						serial.setSpeed(0, 0);//interruption
						break;
			case 'w':	serial.setSpeed(mot1, mot2);//forward
						sign = 1;
						break;
			case 's':	serial.setSpeed(-mot1, -mot2);//back
						sign = -1;
						break;
			case 'a':	serial.rotate(sign * angle);//left
						sleep(times);
						serial.setSpeed(sign * mot1, sign * mot2);
						break;
			case 'd':	serial.rotate(-sign * angle);//right
						sleep(times);
						serial.setSpeed(sign * mot1, sign * mot2);
						break;
		}
	}
	return 0;
}