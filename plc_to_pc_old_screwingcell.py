import snap7
from snap7 import util
from snap7.types import *
from snap7.util import *



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

def readBool2(db_number, start_offset, bit_offset):
	reading = client.db_read(db_number, start_offset, 1)  
	a = snap7.util.get_bool(reading, 0, bit_offset)
	print('DB Number: ' + str(db_number) + ' Bit: ' + str(start_offset) + '.' + str(bit_offset) + ' Value: ' + str(a))
	return a

# lasse have not tested read and write momery yet
def readMemory(start_address,length):
	reading = client.read_area(snap7.types.Areas.MK, 0, start_address, length)
	value = struct.unpack('>f', reading)  # big-endian / if not work try to use little-endian
	print('Start Address: ' + str(start_address) + ' Value: ' + str(value))

def writeMemory(start_address,length,value):
	client.mb_write(start_address, length, bytearray(struct.pack('>f', value)))  # big-endian
	print('Start Address: ' + str(start_address) + ' Value: ' + str(value))


client = snap7.client.Client()
client.connect('172.20.1.148',0,1)
db_number = 19
start_offset = 0
bit_offset = 0

if client.get_connected():
	print("connected")
	while(1):
	    time.sleep(1)
	    if(readBool2(db_number,start_offset,bit_offset)):
		    print("process started")
