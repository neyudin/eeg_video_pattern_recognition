import time
import serial

ser = serial.Serial(
    port='COM1',
    baudrate=57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS,
    xonxoff=False,
    timeout=1,
    rtscts=False,
    dsrdtr=False
)

ser1 = serial.Serial(
    port='COM2',
    baudrate=57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS,
    xonxoff=False,
    timeout=1,
    rtscts=False,
    dsrdtr=False
)

if ser.isOpen():
    print(ser.name + ' is open...')
    
    if ser1.isOpen():
        print(ser1.name + ' is open...\n')
        
        while True:
            cmd = raw_input("Enter command to write to " + ser.name + " or 'exit': ")
            if cmd == 'exit':
                ser.close()
                ser1.close()
                exit()
            else:
                ser.write(cmd.encode('ascii') + '\r\n')
                out = ''
                time.sleep(1)
                while ser1.inWaiting() > 0:
                    out += ser1.read(1)
                if out != '':
                    print('Receiving from ' + ser1.name + '... ' + out)
