#include "cknetserial.h"
#include <iostream>

CKNetSerial::CKNetSerial(const std::string& devname, serial_port_base::baud_rate baud_rate,
			serial_port_base::parity opt_parity, serial_port_base::character_size opt_csize, 
			serial_port_base::flow_control opt_flow, serial_port_base::stop_bits opt_stop, float radius)
        : io(), serial(io, devname), robot_radius(radius)
{
    serial.set_option(baud_rate);
    serial.set_option(opt_parity);
    serial.set_option(opt_csize);
    serial.set_option(opt_flow);
    serial.set_option(opt_stop);
};

bool CKNetSerial::setPosition(float mot1, float mot2)
{
    stringstream command;
    command << "C," << FROM_MM_TO_UNITS(mot1) << "," << FROM_MM_TO_UNITS(mot2) << "\r\n";
   // cout << command.str() << endl;
    writeString(command.str());
    response = readLine();
   // cout << response << endl;
    return (response.compare("c") == 0);
}

bool CKNetSerial::move(float dist)
{
    setPositionCounter(0,0);
    return setPosition(dist, dist);
}

bool CKNetSerial::rotate(float angle)
{
    if(setPositionCounter(0,0))
    {
	//cout << angle*robot_radius << endl;
	return setPosition(-angle*robot_radius, angle*robot_radius);
    }
    return false;
}

bool CKNetSerial::setPositionCounter(float mot1, float mot2)
{
    stringstream command;
    command << "G," << FROM_MM_TO_UNITS(mot1) << "," << FROM_MM_TO_UNITS(mot2) << "\r\n";
    //cout << command.str() << endl;
    writeString(command.str());
    response = readLine();
   // cout << response << endl;
    return (response.compare("g") == 0);   
}

bool CKNetSerial::setTrapezoidProfile(float max_speed1, float acc1, float max_speed2, float acc2)
{
    stringstream command;
    command << "J," << FROM_MM_S_TO_UNITS_S(max_speed1) << "," << FROM_MM_SS_TO_UNITS_SS(acc1) << "," << FROM_MM_S_TO_UNITS_S(max_speed2) << "," << FROM_MM_SS_TO_UNITS_SS(acc2) << "\r\n";
    //cout << command.str() << endl;
    writeString(command.str());
    response = readLine();
    //cout << response << endl;
    cout << command.str();
    return (response.compare("j") == 0);     
}

bool CKNetSerial::setDefaultTrapezoidProfile()
{
    stringstream command;
    command << "J," << 20 << "," << 64 << "," << 20 << "," << 64 << "\r\n";
    //cout << command.str() << endl;
    writeString(command.str());
    response = readLine();
    //cout << response << endl;
    cout << command.str();
    return (response.compare("j") == 0);     
}

bool CKNetSerial::getObjectPresence()
{
    stringstream command;
    command << "T,1,G" << "\r\n";
    writeString(command.str());
    string response = readLine();
    //cout << response << endl;
    //usleep(600000);
    return (response.compare("t,1,g,0") != 0);   
}

bool CKNetSerial::setArmPosition(int pos)
{
    stringstream command;
    command << "T,1,E," << pos << "\r\n";
    usleep(1000000);
    writeString(command.str());
    response = readLine();
//    cout << response << endl;
    usleep(1000000);
    return (response.compare("t,1,e") == 0);       
}

bool CKNetSerial::closeGripper()
{
    stringstream command;
    command << "T,1,D," << 1 << "\r\n";
    writeString(command.str());
    response = readLine();
//    cout << response << endl;
    usleep(600000);
    return (response.compare("t,1,d") == 0);       
}

bool CKNetSerial::openGripper()
{
    stringstream command;
    command << "T,1,D," << 0 << "\r\n";
    writeString(command.str());
    response = readLine();
    cout << response << endl;
    usleep(600000);
    return (response.compare("t,1,d") == 0);       
}

bool CKNetSerial::getSpeed(float & mot1, float& mot2)
{
    stringstream command;
    command << "E" << "\r\n";
    writeString(command.str());
    response = readLine();
    //cout << response << endl;    
    int imot1, imot2;
    int res = sscanf(response.c_str(),"e,%d,%d", &imot1, &imot2); //must be assigned two varibles
    mot1 = FROM_UNITS_S_TO_MM_S(imot1);
    mot2 = FROM_UNITS_S_TO_MM_S(imot2);
    return (res == 2);       
}

bool CKNetSerial::getArmPosition(int &pos)
{
    stringstream command;
    command << "T,1,H," << 1 << "\r\n";
    writeString(command.str());
    response = readLine();
//    cout << response << endl;
    int res = sscanf(response.c_str(),"t,1,h,%d", &pos); 
    return (res == 1);      
}

bool CKNetSerial::getGripperPos(int &pos)
{
    stringstream command;
    command << "T,1,H," << 0 << "\r\n";
    writeString(command.str());
    response = readLine();
    //cout << response << endl;
    int res = sscanf(response.c_str(),"t,1,h,%d", &pos); 
    return (res == 1);    
}

bool CKNetSerial::setSpeed(float mot1, float mot2)
{
    stringstream command;
    command << "D," << FROM_MM_S_TO_UNITS_S(mot1) << "," << FROM_MM_S_TO_UNITS_S(mot2) << "\r\n";
   // cout << command.str() << endl;
    writeString(command.str());
    response = readLine();
    //cout << response << endl;
    return (response.compare("d") == 0);    
}



bool CKNetSerial::getSensorsInfo(int sens[8])
{
    stringstream command;
    command << "N\r\n";
   // cout << command.str() << endl;
    writeString(command.str());
    response = readLine();
   // cout << response << endl;
    int res = sscanf(response.c_str(),"n,%d,%d,%d,%d,%d,%d,%d,%d", &sens[0], &sens[1], &sens[2], &sens[3], &sens[4], &sens[5], &sens[6], &sens[7]);
    return (response.compare("n") == 0);    

}

bool CKNetSerial::setSpeedi(int mot1, int mot2)
{
    stringstream command;
    command << "D," << mot1 << "," << mot2 << "\r\n";
   // cout << command.str() << endl;
    writeString(command.str());
    response = readLine();
   // cout << response << endl;
    return (response.compare("d") == 0);  
}

