#ifndef CKNETSERIAL_H
#define CKNETSERIAL_H

#include <boost/asio.hpp>
#include <iostream>


using namespace std;
using namespace boost::asio;

#define FROM_UNITS_TO_MM(x) 		x*0.08
#define FROM_MM_TO_UNITS(x) 		(int)(x*12.5)
#define FROM_MM_S_TO_UNITS_S(x)		(int)(x*0.125)
#define FROM_UNITS_S_TO_MM_S(x)		x*8
#define FROM_MM_SS_TO_UNITS_SS(x)	(int)(x*8/25)
#define KHEPERA_RADIUS			26.5f
#define HELLO_MSG_NUM_LINES		17
#define EXCEPTION_MSG_NUM_LINES		25

class CKNetSerial
{
    float robot_radius;
    string response;
public:
    /**
     * Constructor.
     * \param port device name, example "/dev/ttyUSB0" or "COM4"
     * \param baud_rate communication speed, example 9600 or 115200
     * \throws boost::system::system_error if cannot open the
     * serial device
     */
    CKNetSerial(const std::string& devname,  serial_port_base::baud_rate baud_rate,
        boost::asio::serial_port_base::parity opt_parity=
            boost::asio::serial_port_base::parity(
                boost::asio::serial_port_base::parity::none),
        boost::asio::serial_port_base::character_size opt_csize=
            boost::asio::serial_port_base::character_size(8),
        boost::asio::serial_port_base::flow_control opt_flow=
            boost::asio::serial_port_base::flow_control(
                boost::asio::serial_port_base::flow_control::none),
        boost::asio::serial_port_base::stop_bits opt_stop=
            boost::asio::serial_port_base::stop_bits(
                boost::asio::serial_port_base::stop_bits::one), float radius = KHEPERA_RADIUS);


    /**
     * Write a string to the serial device.
     * \param s string to write
     * \throws boost::system::system_error on failure
     */
    void writeString(std::string s)
    {
        boost::asio::write(serial,boost::asio::buffer(s.c_str(),s.size()));
    }

    /**
     * Blocks until a line is received from the serial device.
     * Eventual '\n' or '\r\n' characters at the end of the string are removed.
     * \return a string containing the received line
     * \throws boost::system::system_error on failure
     */
    std::string readLine()
    {
        //Reading data char by char, code is optimized for simplicity, not speed
        char c;
        std::string result;
        for(;;)
        {
            read(serial,buffer(&c,1));
            switch(c)
            {
                case '\r':
                    break;
                case '\n':
                    return result;
                default:
                    result+=c;
            }
        }
    }
    
    bool setPosition(float mot1, float mot2);
    bool setPositionCounter(float mot1, float mot2);
    bool setSpeed (float mot1, float mot2);
    bool setSpeedi(int arg1, int arg2);
    bool setTrapezoidProfile(float acc1, float max_speed1, float acc2, float msx_speed2);
    bool setDefaultTrapezoidProfile();
    bool setArmPosition(int pos);
    
    bool getObjectPresence();
    bool getArmPosition(int& pos);
    bool getSpeed(float& mot1, float& mot2);
    bool getSensorsInfo(int sens[8]);

    bool getGripperPos(int& pos);
    bool closeGripper();
    bool openGripper();
    bool move(float dist); // mm
    bool rotate(float angle); // rad

    void printResponse()
    {
        char c;
	int count_lines = 1;
        std::string result;
        for(;;)
        {
            read(serial, buffer(&c,1));
            switch(c)
            {
                case '\r':
                    break;
                case '\n':
                    count_lines++;
		    if(count_lines >= HELLO_MSG_NUM_LINES)
		    {
			break;
		    }
                default:
                    result+=c;
            }
        }
	cout << "Response: " << result << endl;
    }

    void flush()
    {
	for (int i = 0; i < 17; i++)
	{
	    response = readLine();
	    cout << response << endl;
	}
    }
    
//     void flushResponse()
//     {
//         char c;
//         std::string result;
//         for(;;)
//         {
//             async_read(serial,buffer(&c,1));
//             switch(c)
//             {
//                 case '\r':
//                     break;
//                 case '\n':
//                     return result;
//                 default:
//                     result+=c;
//             }
//         }
//     }

private:
    boost::asio::io_service io;
    boost::asio::serial_port serial;
};

#endif // CKNETSERIAL_H
