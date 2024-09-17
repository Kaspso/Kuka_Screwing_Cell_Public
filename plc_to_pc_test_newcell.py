import snap7
from snap7 import util
from snap7.types import *
from snap7.util import *
import time



## når denne skal bruges skal du have two ip address på samme interface, en 192.168.1.100 og en 192.168.0.135

# to configure the PLC to be able to communicate see this link: https://snap7.sourceforge.net/snap7_client.html#1200_1500
# the minimum amount of data being read or written to a plc is 1 byte
# snap7 documentation can be found here https://buildmedia.readthedocs.org/media/pdf/python-snap7/latest/python-snap7.pdf or just google it
# see exampel link: https://github.com/Mareh07/plcwars-python-snap7/blob/main/read_write_snap7.py
def writeBool(db_number, start_offset, bit_offset, value):
	reading = client.db_read(db_number, start_offset, 1)    # (db number, start offset, read 1 byte)
	snap7.util.set_bool(reading, 0, bit_offset, value)   # (value 1= true;0=false) (bytearray_: bytearray, byte_index: int, bool_index: int, value: bool)
	client.db_write(db_number, start_offset, reading)       #  write back the bytearray and now the boolean value is changed in the PLC.
	return None

def readBool(db_number, start_offset, bit_offset):
	reading = client.db_read(db_number, start_offset, 1)  
	a = snap7.util.get_bool(reading, 0, bit_offset)
	print('DB Number: ' + str(db_number) + ' Bit: ' + str(start_offset) + '.' + str(bit_offset) + ' Value: ' + str(a))
	return None

# lasse have not tested read and write momery yet
def readMemory(start_address,length):
	reading = client.read_area(snap7.types.Areas.MK, 0, start_address, length)
	value = struct.unpack('>f', reading)  # big-endian / if not work try to use little-endian
	print('Start Address: ' + str(start_address) + ' Value: ' + str(value))

def writeMemory(start_address,length,value):
	client.mb_write(start_address, length, bytearray(struct.pack('>f', value)))  # big-endian
	print('Start Address: ' + str(start_address) + ' Value: ' + str(value))


client = snap7.client.Client()
client.connect('192.168.0.1',0,1)




db_number = 101
start_offset = 836
bit_offset = 0


if client.get_connected():
    #print(client.db_read(5, 0, 18))
    #db = client.db_read(5, 0, 4)
    #t = util.get_real(db, 0)
    #print(t)
    print("connected")
    time.sleep(2)
    
    
    start = time.time()
    for i in range(100):
		
        writeBool(db_number, start_offset, bit_offset, True)
        readBool(db_number, start_offset, 0)
    end = time.time()
    print((end - start)/100)
    
    #readBool(db_number, start_offset, bit_offset)
    #writeBool(db_number, start_offset, bit_offset, True)
	#readBool(db_number, start_offset, bit_offset)
    # setting fixture on and off here below
    #readBool(23,122,0)
    #writeBool(23,122,0,1)
    #time.sleep(2)
    #writeBool(23,122,0,0)
    #readBool(23,122,0)
    print('Done')
    #db = client.db_read(101,0, 1)

    
    client.disconnect()
    client.destroy()

