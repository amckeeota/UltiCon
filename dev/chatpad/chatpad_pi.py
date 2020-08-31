import sys
import serial
import time, threading
import uinput

events = (
    uinput.KEY_A,
    uinput.KEY_B,
    uinput.KEY_C,
    uinput.KEY_D,
    uinput.KEY_E,
    uinput.KEY_F,
    uinput.KEY_G,
    uinput.KEY_H,
    uinput.KEY_I,
    uinput.KEY_J,
    uinput.KEY_K,
    uinput.KEY_L,
    uinput.KEY_M,
    uinput.KEY_N,
    uinput.KEY_O,
    uinput.KEY_P,
    uinput.KEY_Q,
    uinput.KEY_R,
    uinput.KEY_S,
    uinput.KEY_T,
    uinput.KEY_U,
    uinput.KEY_V,
    uinput.KEY_W,
    uinput.KEY_X,
    uinput.KEY_Y,
    uinput.KEY_Z,
    uinput.KEY_1,
    uinput.KEY_2,
    uinput.KEY_3,
    uinput.KEY_4,
    uinput.KEY_5,
    uinput.KEY_6,
    uinput.KEY_7,
    uinput.KEY_8,
    uinput.KEY_9,
    uinput.KEY_0,
    uinput.KEY_ESC,
    uinput.KEY_MINUS,
    uinput.KEY_EQUAL,
    uinput.KEY_BACKSPACE,
    uinput.KEY_TAB,
    uinput.KEY_LEFTBRACE,
    uinput.KEY_RIGHTBRACE,
    uinput.KEY_ENTER,
    uinput.KEY_LEFTCTRL,
    uinput.KEY_SEMICOLON,
    uinput.KEY_APOSTROPHE,
    uinput.KEY_LEFTSHIFT,
    uinput.KEY_BACKSLASH,
    uinput.KEY_COMMA,
    uinput.KEY_DOT,
    uinput.KEY_SLASH,
    uinput.KEY_CAPSLOCK,
    uinput.KEY_SPACE,
    uinput.KEY_F1,
    uinput.KEY_F2,
    uinput.KEY_F3,
    uinput.KEY_F4,
    uinput.KEY_F5,
    uinput.KEY_F6,
    uinput.KEY_F7,
    uinput.KEY_F8,
    uinput.KEY_F9,
    uinput.KEY_F10,
    uinput.KEY_KPASTERISK,
    uinput.KEY_HOME,
    uinput.KEY_END,
    uinput.KEY_LEFT,
    uinput.KEY_RIGHT,
    uinput.KEY_DOLLAR
    )

time.sleep(1)
port = serial.Serial("/dev/ttyS0", 19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
device = uinput.Device(events)

CHAR_EVENT0 = 0xb4
CHAR_EVENT1 = 0xc5

char_lookup = {
#row 1
    0x17 : (uinput.KEY_1, 0),
    0x16 : (uinput.KEY_2, 0),
    0x15 : (uinput.KEY_3, 0),
    0x14 : (uinput.KEY_4, 0),
    0x13 : (uinput.KEY_5, 0),
    0x12 : (uinput.KEY_6, 0),
    0x11 : (uinput.KEY_7, 0),
    0x67 : (uinput.KEY_8, 0),
    0x66 : (uinput.KEY_9, 0),
    0x65 : (uinput.KEY_0, 0),
#row 2
    0x27 : (uinput.KEY_Q, 0),
    0x26 : (uinput.KEY_W, 0),
    0x25 : (uinput.KEY_E, 0),
    0x24 : (uinput.KEY_R, 0),
    0x23 : (uinput.KEY_T, 0),
    0x22 : (uinput.KEY_Y, 0),
    0x21 : (uinput.KEY_U, 0),
    0x76 : (uinput.KEY_I, 0),
    0x75 : (uinput.KEY_O, 0),
    0x64 : (uinput.KEY_P, 0),
#row 3
    0x37 : (uinput.KEY_A, 0),
    0x36 : (uinput.KEY_S, 0),
    0x35 : (uinput.KEY_D, 0),
    0x34 : (uinput.KEY_F, 0),
    0x33 : (uinput.KEY_G, 0),
    0x32 : (uinput.KEY_H, 0),
    0x31 : (uinput.KEY_J, 0),
    0x77 : (uinput.KEY_K, 0),
    0x72 : (uinput.KEY_L, 0),
    0x62 : (uinput.KEY_COMMA, 0),
#row 4
    0x46 : (uinput.KEY_Z, 0),
    0x45 : (uinput.KEY_X, 0),
    0x44 : (uinput.KEY_C, 0),
    0x43 : (uinput.KEY_V, 0),
    0x42 : (uinput.KEY_B, 0),
    0x41 : (uinput.KEY_N, 0),
    0x52 : (uinput.KEY_M, 0),
    0x53 : (uinput.KEY_DOT, 0),
    0x63 : (uinput.KEY_ENTER, 0),
#row 5
    0x55 : (uinput.KEY_LEFT, 0),
    0x54 : (uinput.KEY_SPACE, 0),
    0x51 : (uinput.KEY_RIGHT, 0),
    0x71 : (uinput.KEY_BACKSPACE, 0)
}

people_lookup = {
#row 1
    0x17 : (uinput.KEY_1, uinput.KEY_LEFTCTRL),
    0x16 : (uinput.KEY_2, uinput.KEY_LEFTCTRL),
    0x15 : (uinput.KEY_3, uinput.KEY_LEFTCTRL),
    0x14 : (uinput.KEY_4, uinput.KEY_LEFTCTRL),
    0x13 : (uinput.KEY_5, uinput.KEY_LEFTCTRL),
    0x12 : (uinput.KEY_6, uinput.KEY_LEFTCTRL),
    0x11 : (uinput.KEY_7, uinput.KEY_LEFTCTRL),
    0x67 : (uinput.KEY_8, uinput.KEY_LEFTCTRL),
    0x66 : (uinput.KEY_9, uinput.KEY_LEFTCTRL),
    0x65 : (uinput.KEY_0, uinput.KEY_LEFTCTRL),
#row 2
    0x27 : (uinput.KEY_Q, uinput.KEY_LEFTCTRL),
    0x26 : (uinput.KEY_W, uinput.KEY_LEFTCTRL),
    0x25 : (uinput.KEY_E, uinput.KEY_LEFTCTRL),
    0x24 : (uinput.KEY_R, uinput.KEY_LEFTCTRL),
    0x23 : (uinput.KEY_T, uinput.KEY_LEFTCTRL),
    0x22 : (uinput.KEY_Y, uinput.KEY_LEFTCTRL),
    0x21 : (uinput.KEY_U, uinput.KEY_LEFTCTRL),
    0x76 : (uinput.KEY_I, uinput.KEY_LEFTCTRL),
    0x75 : (uinput.KEY_O, uinput.KEY_LEFTCTRL),
    0x64 : (uinput.KEY_P, uinput.KEY_LEFTCTRL),
#row 3
    0x37 : (uinput.KEY_A, uinput.KEY_LEFTCTRL),
    0x36 : (uinput.KEY_S, uinput.KEY_LEFTCTRL),
    0x35 : (uinput.KEY_D, uinput.KEY_LEFTCTRL),
    0x34 : (uinput.KEY_F, uinput.KEY_LEFTCTRL),
    0x33 : (uinput.KEY_G, uinput.KEY_LEFTCTRL),
    0x32 : (uinput.KEY_H, uinput.KEY_LEFTCTRL),
    0x31 : (uinput.KEY_J, uinput.KEY_LEFTCTRL),
    0x77 : (uinput.KEY_K, uinput.KEY_LEFTCTRL),
    0x72 : (uinput.KEY_L, uinput.KEY_LEFTCTRL),
    0x62 : (uinput.KEY_COMMA, uinput.KEY_LEFTCTRL),
#row 4
    0x46 : (uinput.KEY_Z, uinput.KEY_LEFTCTRL),
    0x45 : (uinput.KEY_X, uinput.KEY_LEFTCTRL),
    0x44 : (uinput.KEY_C, uinput.KEY_LEFTCTRL),
    0x43 : (uinput.KEY_V, uinput.KEY_LEFTCTRL),
    0x42 : (uinput.KEY_B, uinput.KEY_LEFTCTRL),
    0x41 : (uinput.KEY_N, uinput.KEY_LEFTCTRL),
    0x52 : (uinput.KEY_M, uinput.KEY_LEFTCTRL),
    0x53 : (uinput.KEY_DOT, uinput.KEY_LEFTCTRL),
    0x63 : (uinput.KEY_ENTER, uinput.KEY_LEFTCTRL),
#row 5
    0x55 : (uinput.KEY_LEFT, uinput.KEY_LEFTCTRL),
    0x54 : (uinput.KEY_SPACE, uinput.KEY_LEFTCTRL),
    0x51 : (uinput.KEY_RIGHT, uinput.KEY_LEFTCTRL),
    0x71 : (uinput.KEY_BACKSPACE, uinput.KEY_LEFTCTRL)
}

shift_char_lookup = {
#row 2
    0x27 : (uinput.KEY_LEFTSHIFT, uinput.KEY_Q),
    0x26 : (uinput.KEY_LEFTSHIFT, uinput.KEY_W),
    0x25 : (uinput.KEY_LEFTSHIFT, uinput.KEY_E),
    0x24 : (uinput.KEY_LEFTSHIFT, uinput.KEY_R),
    0x23 : (uinput.KEY_LEFTSHIFT, uinput.KEY_T),
    0x22 : (uinput.KEY_LEFTSHIFT, uinput.KEY_Y),
    0x21 : (uinput.KEY_LEFTSHIFT, uinput.KEY_U),
    0x76 : (uinput.KEY_LEFTSHIFT, uinput.KEY_I),
    0x75 : (uinput.KEY_LEFTSHIFT, uinput.KEY_O),
    0x64 : (uinput.KEY_LEFTSHIFT, uinput.KEY_P),
#row 3
    0x37 : (uinput.KEY_LEFTSHIFT, uinput.KEY_A),
    0x36 : (uinput.KEY_LEFTSHIFT, uinput.KEY_S),
    0x35 : (uinput.KEY_LEFTSHIFT, uinput.KEY_D),
    0x34 : (uinput.KEY_LEFTSHIFT, uinput.KEY_F),
    0x33 : (uinput.KEY_LEFTSHIFT, uinput.KEY_G),
    0x32 : (uinput.KEY_LEFTSHIFT, uinput.KEY_H),
    0x31 : (uinput.KEY_LEFTSHIFT, uinput.KEY_J),
    0x77 : (uinput.KEY_LEFTSHIFT, uinput.KEY_K),
    0x72 : (uinput.KEY_LEFTSHIFT, uinput.KEY_L),
#row 4
    0x46 : (uinput.KEY_LEFTSHIFT, uinput.KEY_Z),
    0x45 : (uinput.KEY_LEFTSHIFT, uinput.KEY_X),
    0x44 : (uinput.KEY_LEFTSHIFT, uinput.KEY_C),
    0x43 : (uinput.KEY_LEFTSHIFT, uinput.KEY_V),
    0x42 : (uinput.KEY_LEFTSHIFT, uinput.KEY_B),
    0x41 : (uinput.KEY_LEFTSHIFT, uinput.KEY_N),
    0x52 : (uinput.KEY_LEFTSHIFT, uinput.KEY_M),
    0x63 : (uinput.KEY_ENTER, 0),
#row 5
    0x55 : (uinput.KEY_LEFT, 0),
    0x54 : (uinput.KEY_SPACE, 0),
    0x51 : (uinput.KEY_RIGHT, 0),
    0x71 : (uinput.KEY_BACKSPACE, 0)
}

square_lookup = {
    0x17 : (uinput.KEY_F1, 0),
    0x16 : (uinput.KEY_F2, 0),
    0x15 : (uinput.KEY_F3, 0),
    0x14 : (uinput.KEY_F4, 0),
    0x13 : (uinput.KEY_F5, 0),
    0x12 : (uinput.KEY_F6, 0),
    0x11 : (uinput.KEY_F7, 0),
    0x67 : (uinput.KEY_F8, 0),
    0x66 : (uinput.KEY_F9, 0),
    0x65 : (uinput.KEY_F10, 0),
#row 2
    0x27 : (uinput.KEY_LEFTSHIFT, uinput.KEY_1),
    0x26 : (uinput.KEY_LEFTSHIFT, uinput.KEY_2),
    0x25 : (uinput.KEY_LEFTSHIFT, uinput.KEY_4),
    0x24 : (uinput.KEY_LEFTSHIFT, uinput.KEY_3),
    0x23 : (uinput.KEY_LEFTSHIFT, uinput.KEY_5),
    0x22 : (uinput.KEY_LEFTSHIFT, uinput.KEY_6),
    0x21 : (uinput.KEY_LEFTSHIFT, uinput.KEY_7),
    0x76 : (uinput.KEY_LEFTSHIFT, uinput.KEY_8),
    0x75 : (uinput.KEY_LEFTSHIFT, uinput.KEY_9),
    0x64 : (uinput.KEY_LEFTSHIFT, uinput.KEY_0),
#row 3
    #0x37 : '~',
    0x35 : (uinput.KEY_LEFTBRACE, 0),
    0x34 : (uinput.KEY_RIGHTBRACE, 0),
    0x32 : (uinput.KEY_SLASH, 0),
    0x31 : (uinput.KEY_APOSTROPHE, 0),
    0x77 : (uinput.KEY_LEFTSHIFT, uinput.KEY_LEFTBRACE),
    0x72 : (uinput.KEY_LEFTSHIFT, uinput.KEY_RIGHTBRACE),
    0x62 : (uinput.KEY_LEFTSHIFT, uinput.KEY_SEMICOLON),
#row 4
    #0x46 : '`',
    0x43 : (uinput.KEY_MINUS, 0),
    0x42 : (uinput.KEY_LEFTSHIFT, uinput.KEY_BACKSLASH),
    0x41 : (uinput.KEY_LEFTSHIFT, uinput.KEY_COMMA),
    0x52 : (uinput.KEY_LEFTSHIFT, uinput.KEY_DOT),
    0x53 : (uinput.KEY_LEFTSHIFT, uinput.KEY_SLASH)
}

circle_lookup = {
#row 2
    0x64 : (uinput.KEY_EQUAL, 0),
#row 3
    0x32 : (uinput.KEY_BACKSLASH, 0),
    0x31 : (uinput.KEY_LEFTSHIFT, uinput.KEY_APOSTROPHE),
    0x62 : (uinput.KEY_SEMICOLON, 0),
#row 4
    0x43 : (uinput.KEY_LEFTSHIFT, uinput.KEY_MINUS),
    0x42 : (uinput.KEY_LEFTSHIFT, uinput.KEY_EQUAL)

}

NONE = 0
UPPER = 1
SQUARE = 2
CIRCLE = 4
PEOPLE = 8

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

def sendToUinput(key1,key2):
    if key2 == 0:
        device.emit_click(key1)
    else:
        device.emit_combo([key1, key2])

def printCode(code, modifier):
    global capslock
    global prev_mod
    if modifier == UPPER:
        if capslock:
            if code in char_lookup:
                press1, press2 = char_lookup[code]
                sendToUinput(press1, press2)
        else:
            if code in shift_char_lookup:
                press1, press2 = shift_char_lookup[code]
                sendToUinput(press1, press2)
    elif modifier == SQUARE:
        if code in square_lookup:
            press1, press2 = square_lookup[code]
            sendToUinput(press1, press2)
    elif modifier == CIRCLE:
        if code in circle_lookup:
            press1, press2 = circle_lookup[code]
            sendToUinput(press1, press2)
    elif modifier == PEOPLE:
        if code in people_lookup:
            press1, press2 = pepole_lookup[code]
            sendToUinput(press1, press2)
    elif modifier == (CIRCLE | UPPER) and prev_mod == 0:
        prev_mod = (CIRCLE | UPPER)
        device.emit_click(uinput.KEY_CAPSLOCK)
        capslock != capslock
    else:
        if code in char_lookup:
            press1, press2 = char_lookup[code]
            sendToUinput(press1, press2)

port.write(initpacket)
time.sleep(1)
sendKeepAlive()
print("Chatpad Loaded")

capsengaged = 0

while True:
    # Read 8 bytes at a time (one frame)
    rcv = port.read(8)
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
