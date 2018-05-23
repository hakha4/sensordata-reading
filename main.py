'''Import libs'''
import sys
import glob
import serial

'''find avaliable ports'''
def serial_ports():


    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return "Avaliable ports : " + str((", ".join(result)))

'''Ask user for port no and baudrate'''

def get_port_properties(prompt):

    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value < 0:
            print("Sorry, your response must not be negative.")
            continue
        else:
            break
    return value
''' find avaliable ports '''
print(serial_ports())
''' user input, later from ini.file ? '''
port = get_port_properties("Please enter portnumber 1,2,3 etc.: ")
port = 'COM' + str(port)
baud = get_port_properties("Please enter Baudrate 9600, 19200, 38400, 57600, 115200: ")

''' open port '''
try:
    ser = serial.Serial(port, baud, timeout=0,parity=serial.PARITY_EVEN, rtscts=1)
    print ("Port open on " + port)
except:
    print("ERROR opening port on " + port)




if __name__ == '__main__':
    pass



