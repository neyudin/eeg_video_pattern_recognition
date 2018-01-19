#!/usr/bin/python

from __future__ import print_function
import platform
if platform.system() == "Windows":
    import socket  # Needed to prevent gevent crashing on Windows. (surfly / gevent issue #459)
import gevent
import numpy as np
import math
import time

from emokit.emotiv import Emotiv
from robot import Khepera2

def main():
    print('Connecting to the robot')
    r = Khepera2()
    if not r.opened():
        print('Something\'s gone wrong with the robot =(')
    
    left, right, angle = 40, 40, math.asin(1.0)
    
    print('Connecting to Emotiv')
    emotiv = Emotiv(display_output=False)
    gevent.spawn(emotiv.setup)
    gevent.sleep(0)
    timestamp = -100
    f7_log = []
    f8_log = []
    f7_mean = 0
    f7_std = 0
    f8_mean = 0
    f8_std = 0
    print('Training')
    
    l_act = False
    r_act = False
    stopped = True
    stopping = False
    lastleft = -100
    lastright = -100
    delay = 10
    leftdelay = False
    rightdelay = False
    pass_packets = 150
    
    while emotiv.running:
        try:
            packet = emotiv.dequeue()
            if timestamp < 0:
                f7_log.append(packet.F7[0])
                f8_log.append(packet.F8[0])
                timestamp += 1
            elif timestamp == 0:
                f7_mean = np.mean(f7_log)
                f7_std = np.std(f7_log)
                f8_mean = np.mean(f8_log)
                f8_std = np.std(f8_log)
                timestamp += 1
                print('Training completed\nF7\t%4d\t%4d\nF8\t%4d\t%4d' % (f7_mean, f7_std, f8_mean, f8_std))
                print('GO')
                #r.setspeed(left, right)
            else:
                if abs(packet.F7[0] - f7_mean) > 15 * f7_std:
                    l_act = True
                    if (timestamp - lastleft) < delay:
                        leftdelay = True
                else:
                    if l_act and not stopping:
                        if not leftdelay:
                            r.rotate(angle)
                            #time.sleep(1)
                            for i in range(pass_packets):
                                packet = emotiv.dequeue()          
                            if not stopped:
                                r.setspeed(left, right)
                        lastleft = timestamp
                    l_act = False
                    leftdelay = False

                if abs(packet.F8[0] - f8_mean) > 12 * f8_std:
                    r_act = True
                    if (timestamp - lastright) < delay:
                        rightdelay = True
                else:
                    if r_act and not stopping:
                        if not rightdelay:
                            r.rotate(-angle)
                            #time.sleep(1)
                            for i in range(pass_packets):
                                packet = emotiv.dequeue()          
                            if not stopped:
                                r.setspeed(left, right)
                        lastright = timestamp
                    rightdelay = False
                    r_act = False
                if l_act and r_act:
                    if not stopping:
                        if stopped:
                            r.setspeed(left, right)
                        else:
                            r.setspeed(0, 0)
                            r.setpositioncounter(0,0)
                        stopped = not stopped
                    stopping = True
                elif not l_act and not r_act:
                    stopping = False
                    
                print('%5d   %5s   %5s   %5s' % (timestamp, 
                                           'Left' if l_act else '',
                                           'Right' if r_act else '', 
                                           'Stop' if l_act and r_act else ''))
                timestamp += 1 
             
        except Exception, ex:
            print(ex)
            
        gevent.sleep(0)
        
    r.setspeed(0,0)
    r.setpositioncounter(0,0)
    r.__del__()
    
        
if __name__ == '__main__':
    main()
