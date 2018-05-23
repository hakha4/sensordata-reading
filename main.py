'''Import libs'''
import sys
import glob
import serial

''' define global variables '''
ser = ''
runMode = True

'''find avaliable ports'''
def serial_ports():
    print("************************************")
    print("Scanning for avaliable port(s) ....")
    print("************************************")
    print()
    print()
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
    return "Avaliable port(s) : " + str((", ".join(result)))

'''Ask user for port no and baudrate'''

def get_port_properties(prompt):

    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Invalid choice")
            continue

        if value < 0:
            print("Invalid choice")
            continue
        else:
            break
    return value
''' find avaliable ports '''
print(serial_ports())
''' user input, later from ini.file ? '''
print()
port = get_port_properties("Please enter portnumber 1,2,3 etc.: ")
port = 'COM' + str(port)
print()
baud = get_port_properties("Please enter Baudrate 9600, 19200, 38400, 57600, 115200: (DEFAULT = 115200)")
print()

''' open port '''
try:
    ser = serial.Serial(port, baud, timeout=0,parity=serial.PARITY_EVEN, rtscts=1)
    print ("Port open on " + port + "    Baudrate = " + str(baud))


except:
    print("ERROR opening port " + port)



def read_serial():
    #ser = ser.readline()
    seq = []
    count = 1

    while True:
        for c in ser.read():
            seq.append(chr(c))  # convert from ANSII
            joined_seq = ''.join(str(v) for v in seq)  # Make a string from array

            if chr(c) == '\n':
                print("Line " + str(count) + ': ' + joined_seq)
                seq = []
                count += 1
                break


def main():
    ''' ToDo : catch keystrokes for exit prog and other features'''
    print()
    print("###############################")
    print("#### For Meny press M #########")
    print("###############################")

    while runMode: # run main over and over. Check for better options
      #print("Waiting for data on serial port " + port + "....")
      read_serial




if __name__ == '__main__': main()




