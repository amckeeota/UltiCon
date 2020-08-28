import serial
import time, threading
port = serial.Serial("/dev/ttyUSB0", 19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

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

port.write(initpacket)
time.sleep(1)
sendKeepAlive()

while True:
	rcv = port.read(10)
	print(rcv)