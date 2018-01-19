import serial

ser = serial.Serial(
    port='COM2',
    baudrate=57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)

if ser.isOpen():
    print(ser.name + ' is open...\n')

    while True:
        out = ''
        while ser.inWaiting() > 0:
            out += ser.read(1)
        if out != '':
            print(out)
