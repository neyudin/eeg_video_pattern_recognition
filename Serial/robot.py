import serial, time, os

class Khepera2:
    """Class to control Khepera 2 robot via serial connection"""
    
    def __init__(self,
                 portname = '',
                 baudrate = 57600,
                 bytesize = serial.EIGHTBITS,
                 parity = serial.PARITY_NONE,
                 stopbits = serial.STOPBITS_TWO,
                 timeout = 2,
                 xonxoff = False,
                 rtscts = False,
                 write_timeout = None,
                 dsrdtr = False,
                 inter_byte_timeout = None,
                 robot_radius = 26.5):
        if portname == '':
            if os.name == 'nt':
                portname = 'COM1'
            elif os.name == 'posix':
                portname = '/dev/ttyUSB0'
            else:
                raise ArgumentError('Please, select correct port')
        self.ser = serial.Serial(portname,
                                 baudrate,
                                 bytesize,
                                 parity,
                                 stopbits,
                                 timeout,
                                 xonxoff,
                                 rtscts,
                                 write_timeout,
                                 dsrdtr,
                                 inter_byte_timeout)
        self.radius = robot_radius

    def __del__(self):
        """Delete object and close serial connection\nTakes none and returns void"""
        self.ser.close()

    def opened(self):
        """Test serial connection\nTakes none and returns bool"""
        return self.ser.isOpen()
    
    def setspeed(self, left, right):
        """Set speed of left and right engines in mm/s\nTakes 2 floats and returns bool"""
        self.ser.write('D,%i,%i\r\n' % (int(left * 0.125), int(right * 0.125)))
        return ('d\r\n' == self.ser.readline())
    
    def setposition(self, left, right):
        """Set robot position in mm\nTakes 2 floats and returns bool"""
        self.ser.write('C,%i,%i\r\n' % (int(left * 12.5), int(right * 12.5)))
        return ('c\r\n' == self.ser.readline())

    def move(self, distance):
        """Move the robot "distance" mm\nTakes float and returns bool"""
        return self.setposition(distance, distance)

    def setpositioncounter(self, left, right):
        """Set position counter of left and right engines in mm\nTakes 2 floats and returns bool"""
        self.ser.write('G,%i,%i\r\n' % (int(left * 12.5), int(right * 12.5)))
        return ('g\r\n' == self.ser.readline())

    def rotate(self, angle):
        """Rotate robot by an angle in radians\nTakes float and returns bool"""
        if self.setpositioncounter(0,0):
            return self.setposition(-angle * self.radius, angle * self.radius)
        else:
            return False

    def settrapezoidprofile(self, max_left, left_acc, max_right, right_acc):
        """\nTakes 4 floats and returns bool"""
        self.ser.write('J,%i,%i,%i,%i\r\n' % (int(max_left * 0.125), int(left_acc * 8.0/25.0), int(max_right * 0.125), int(right_acc * 8.0/25.0)))
        return ('j\r\n' == self.ser.readline())

    def setdefaulttrapezoidprofile(self):
        """\nTakes none and returns bool"""
        self.ser.write('J,20,64,20,64\r\n')
        return ('j\r\n' == self.ser.readline())

    def setarmposition(self, pos):
        """\nTakes int and returns bool"""
        self.ser.write('T,1,E,%i\r\n' % (pos))
        return ('t,1,e\r\n' == self.ser.readline())

    def closegripper(self):
        """Close gripper\nTakes none and returns bool"""
        self.ser.write('T,1,D,1\r\n')
        time.sleep(0.6)
        return ('t,1,d\r\n' == self.ser.readline())

    def opengripper(self):
        """Open gripper\nTakes none and returns bool"""
        self.ser.write('T,1,D,0\r\n')
        time.sleep(0.6)
        return ('t,1,d\r\n' == self.ser.readline())

    def getobjectpresence(self):
        """State of object in gripper\nTakes none and returns bool"""
        self.ser.write('T,1,G\r\n')
        return ('t,1,g,0' != self.ser.readline())

    def getspeed(self):
        """Get current speed of robot\nTakes none and returns list of floats"""
        self.ser.write('E\r\n')
        line = self.ser.readlie().split(',')
        if line[0] == 'e':
            return [int(line[1]) * 8.0, int(line[2]) * 8.0]
        else:
            raise ResponseError('something wrong with format of response')
    
    def getarmposition(self):
        """Get position of Manipulator\nTakes none and returns int"""
        self.ser.write('T,1,H,1\r\n')
        line = self.ser.readline().split('t,1,h,')
        if line[0] == '':
            return int(line[1])
        else:
            raise ResponseError('something wrong with format of response')

    def getgripperposition(self):
        """Get position of Gripper\nTakes none and returns int"""
        self.ser.write('T,1,H,0\r\n')
        line = self.ser.readline().split('t,1,h,')
        if line[0] == '':
            return int(line[1])
        else:
            raise ResponseError('something wrong with format of response')

    def getsensorsinfo(self):
        """Get info from lightsensors\nTakes none and returns list of ints"""
        self.ser.write('N\r\n')
        line = self.ser.readline().split(',')
        if line[0] == 'n':
            line.pop(0)
            return map(int, line)
        else:
            raise ResponseError('something wrong with format of response')
    
    '''Additional methods'''
    
    def configure(self, Kp, Ki, Kd):
        """Set the proportional (Kp), integral (Ki) and derivate (Kd) parameters of\nthe speed controller.\nTakes 3 ints and returns bool"""
        self.ser.write('A,%i,%i,%i\r\n' % (int(Kp), int(Ki), int(Kd)))
        return ('a\r\n' == self.ser.readline())

    def configuredefaults(self):
        """Invokes configure() with default arguments\nTakes none and returns bool"""
        return self.configure(3800, 800, 100)

    def readsoftver(self):
        """Gives the software version stored in the robot's EPROM\nTakes none and returns list of strings"""
        self.ser.write('B\r\n')
        line = self.ser.readline().split(',')
        if line[0] == 'b':
            return [line[1], line[2][:-2]]
        else:
            raise ResponseError('something wrong with format of response')

    def configurepid(self, Kp, Ki, Kd):
        """Set the proportional (Kp), integral (Ki) and derivate (Kd)\nparameters of the position regulator.\nTakes 3 ints and returns bool"""
        self.ser.write('F,%i,%i,%i\r\n' % (int(Kp), int(Ki), int(Kd)))
        return ('f\r\n' == self.ser.readline())

    def configuredefaultpid(self):
        """Invokes configurepid() with default arguments\nTakes none and returns bool"""
        return configurepid(3000, 20, 4000)

    def readposition(self):
        """Read the 32 bit position counter of the two motors in mm. \nThe unit is the pulse, that corresponds to 0.08 mm.\nTakes none and returns list of floats"""
        self.ser.write('H\r\n')
        line = self.ser.readline().split(',')
        if line[0] == 'h':
            return [float(line[1]) * 0.08, float(line[2]) * 0.08]
        else:
            raise ResponseError('something wrong with format of response')

    def readadinput(self, channel_number):
        """\nTakes int and returns float"""
        self.ser.write('I,%i\r\n' % (int(channel_number)))
        line = self.ser.readline().split(',')
        if line[0] == 'i':
            return float(line[1])
        else:
            raise ResponseError('something wrong with format of response')

    def readmotionstat(self):
        """\nTakes none and returns list of ints"""
        self.ser.write('K\r\n')
        line = self.ser.readline().split(',')
        if line[0] == 'k':
            line.pop(0)
            return map(int, line)
        else:
            raise ResponseError('something wrong with format of response')

    def changeledstate(self, led_num, act_num):
        """\nTakes 2 ints and returns bool"""
        self.ser.write('L,%i,%i\r\n' % (int(led_num), int(act_num)))
        return ('l\r\n' == self.ser.readline())

    def readambientsensors(self):
        """\nTakes none and returns list of ints"""
        self.ser.write('O\r\n')
        line = self.ser.readline().split(',')
        if line[0] == 'n':
            line.pop(0)
            return map(int, line)
        else:
            raise ResponseError('something wrong with format of response')

    def setpwm(self, left_pwm, right_pwm):
        """\nTakes 2 ints and returns bool"""
        self.ser.write('P,%i,%i\r\n' % (int(left_pwm), int(right_pwm)))
        return ('p\r\n' == self.ser.readline())

    def readbusbyte(self, rel_addr):
        """\nTakes int and returns int"""
        self.ser.write('R,%i\r\n' % (int(rel_addr)))
        line = self.ser.readline().split(',')
        if line[0] == 'r':
            return int(line[1])
        else:
            raise ResponseError('something wrong with format of response')

    def sendmsgtoturret(self, tur_id, cmd):
        """More common and less safe method\nTakes int and string and returns bool"""
        self.ser.write('T,%i,%s\r\n' % (int(tur_id), str(cmd)))
        return ('t' == self.ser.readline().split(',')[0])

    def writebusbyte(self, data, rel_addr):
        """\nTakes 2 ints and returns bool"""
        self.ser.write('W,%i,%i\r\n' % (int(data), int(rel_addr)))
        return ('w\r\n' == self.ser.readline())

if __name__ == "__main__":
    import math

    r = Khepera2()
    if r.opened():
        sign, times, left, right, angle = 1, 1, 40, 40, math.asin(1.0)
        cmd = raw_input("enter\n'+' to start work\nelse character to set configs\n\n")
    
        if cmd != '+':
            print("settings mode\nenter\n't' to change waiting limit\n's' to change motors' speeds\n'a' to change rotation angle\nelse character to exit settings mode\n")
            while cmd != '+':
                cmd = raw_input()
                if cmd == 't':
                    times = int(input())
                elif cmd == 's':
                    left = int(input())
                    right = int(input())
                elif cmd == 'a':
                    angle = float(input())
                else:
                    print('setting saved\n')
                    cmd = '+'
        
        print("control mode\nenter\n'w' to move forward\n'a' to move left\n's' to move back\n'd' to move right\n'q' to stop\nelse character to finish work\n")
        while True:
            cmd = raw_input()
            if cmd == 'q':
                #interruption
                r.setpositioncounter(0,0)
                r.setspeed(0,0)
            elif cmd == 'w':
                #forward
                r.setspeed(left, right)
                sign = 1
            elif cmd == 's':
                #back
                r.setspeed(-left, -right)
                sign = -1
            elif cmd == 'a':
                #left rotate and move
                r.rotate(sign * angle)
                time.sleep(1)
                #r.setspeed(sign * left, sign * right)
            elif cmd == 'd':
                #right rotate and move
                r.rotate(-sign * angle)
                time.sleep(1)
                #r.setspeed(sign * left, sign * right)
            else:
                r.setspeed(0,0)
                r.setpositioncounter(0,0)
                r.__del__()
                exit()
