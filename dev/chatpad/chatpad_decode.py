import sys
import serial
import time, threading
port = serial.Serial("/dev/ttyUSB0", 19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

CHAR_EVENT0 = 0xb4
CHAR_EVENT1 = 0xc5

char_lookup = {
#row 1
    0x17 : '1',
    0x16 : '2',
    0x15 : '3',
    0x14 : '4',
    0x13 : '5',
    0x12 : '6',
    0x11 : '7',
    0x67 : '8',
    0x66 : '9',
    0x65 : '0',
#row 2
    0x27 : 'q',
    0x26 : 'w',
    0x25 : 'e',
    0x24 : 'r',
    0x23 : 't',
    0x22 : 'y',
    0x21 : 'u',
    0x76 : 'i',
    0x75 : 'o',
    0x64 : 'p',
#row 3
    0x37 : 'a',
    0x36 : 's',
    0x35 : 'd',
    0x34 : 'f',
    0x33 : 'g',
    0x32 : 'h',
    0x31 : 'j',
    0x77 : 'k',
    0x72 : 'l',
    0x62 : ',',
#row 4
    0x46 : 'z',
    0x45 : 'x',
    0x44 : 'c',
    0x43 : 'v',
    0x42 : 'b',
    0x41 : 'n',
    0x52 : 'm',
    0x53 : '.',
    0x63 : '\n',
#row 5
    0x55 : "left",
    0x54 : ' ',
    0x51 : "right",
    0x71 : '\b'
}

square_lookup = {
#row 2
    0x27 : '!',
    0x26 : '@',
    0x25 : '€',
    0x24 : '#',
    0x23 : '%',
    0x22 : '^',
    0x21 : '&',
    0x76 : '*',
    0x75 : '(',
    0x64 : ')',
#row 3
    0x37 : '~',
    0x36 : 'š',
    0x35 : '{',
    0x34 : '}',
    0x33 : '¨',
    0x32 : '/',
    0x31 : '\'',
    0x77 : '[',
    0x72 : ']',
    0x62 : ':',
#row 4
    0x46 : '`',
    0x45 : '«',
    0x44 : '»',
    0x43 : '-',
    0x42 : '|',
    0x41 : '<',
    0x52 : '>',
    0x53 : '?',
}

circle_lookup = {
#row 2
    0x27 : '¡',
    0x26 : 'å',
    0x25 : 'é',
    0x24 : '$',
    0x23 : 'þ',
    0x22 : 'ý',
    0x21 : 'ú',
    0x76 : 'í',
    0x75 : 'ó',
    0x64 : '=',
#row 3
    0x37 : 'á',
    0x36 : 'ß',
    0x35 : 'ð',
    0x34 : '£',
    0x33 : '¥',
    0x32 : '\\',
    0x31 : '\"',
    0x77 : '',
    0x72 : 'ø',
    0x62 : ';',
#row 4
    0x46 : 'æ',
    0x45 : 'œ',
    0x44 : 'ç',
    0x43 : '_',
    0x42 : '+',
    0x41 : 'ñ',
    0x52 : 'µ',
    0x53 : '¿',

}

NONE = 0
UPPER = 1
SQUARE = 2
CIRCLE = 4

first_char = 0
second_char = 0
prev_mod = 0

capslock = 0


initpacket = bytearray()
initpacket.append(0x87)
initpacket.append(0x02)
initpacket.append(0x8C)
initpacket.append(0x1F)
initpacket.append(0xCC)

keepalive = bytearray()
keepalive.append(0x87)
keepalive.append(0x02)
keepalive.append(0x8C)
keepalive.append(0x1B)
keepalive.append(0xD0)

def sendKeepAlive():
    port.write(keepalive)
    threading.Timer(1, sendKeepAlive).start()

def printNormal(code):
    if code in char_lookup:
        if capslock == 1:
            print(char_lookup[code].upper())
        else:
            print(char_lookup[code])

def printCode(code, modifier):
    global capslock
    global prev_mod
    if modifier == UPPER:
        if code in char_lookup:
            if capslock:
                print(char_lookup[code])
            else:
                print(char_lookup[code].upper())
        else:
            printNormal(code)
    elif modifier == SQUARE:
        if code in square_lookup:
            print(square_lookup[code])
        else:
            printNormal(code)
    elif modifier == CIRCLE:
        if code in circle_lookup:
            print(circle_lookup[code])
        else:
            printNormal(code)
    elif modifier == (CIRCLE | UPPER) and prev_mod == 0:
        prev_mod = (CIRCLE | UPPER)
        if capslock == 0:
            capslock = 1
        else:
            capslock = 0
    else:
        printNormal(code)

port.write(initpacket)
time.sleep(1)
sendKeepAlive()


while True:
    # Read 8 bytes at a time (one frame)
    rcv = port.read(8)
    print(rcv)
    # Check that the frame is valid. If not, resync.

    # Check that this is a character update frame
    if rcv[0] == CHAR_EVENT0 and rcv[1] == CHAR_EVENT1:
        # Check if we will update. Conditions:
        #    1. Print the first char if it was zero before and is not equal to 
        if first_char == 0:
            printCode(rcv[4], rcv[3])
        if second_char == 0:
            printCode(rcv[5], rcv[3])
        # Else just update the chars
        if rcv[3] == 0:
            prev_mod = 0
        first_char = rcv[4]
        second_char = rcv[5]