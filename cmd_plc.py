import snap7
from snap7 import util
from snap7.types import *
from snap7.util import *
import threading
from datetime import datetime
import pandas as pd
import os
import time
import numpy as np
## når denne skal bruges skal du have two ip address på samme interface, en 192.168.1.100 og en 192.168.0.135
## Now only as ip 192.168.1.100

# Data attributes to be collected include torque, depth, angle, angular velocity, angular acceleration, and any other relevant screwing parameters (preset values).
#  Torque DB 101 offset 786 type(real) ish float32
#  Depth DB 101 offset 574 type(real) float32 full up 84.7mm
#  Angle DB 101 offset 838 type(Lreal) 
#  Angular velocity DB 101 offset 842 type(Lreal)
#  Angular acceleration DB 101 offset 846 type(Lreal)

# set fixture DB 102 offset 0 bit_offset 2
# start DB 102 offset 0 bit_offset 0
# reset machine DB102 offset 0 bit_offset 1
# plc program select DB 102 offset 1 bit_offset 0 type(uint8) 
# reset screwdriver DB 102 offset 0 bit_offset 3

# state DB 102 offset 2 bit_offset 0 type(usint/uint8)
# resson DB 102 offset 3 bit_offset 0 type(usint/uint8)

# torque array db 102 offset  10008 bit_offset 0
# depth array db 102 offset 4 bit_offset 0
# angle array db 102 offset 30016 bit_offset 0
# angle velocity array db 102 offset 20012 bit_offset 0
# angle acceleration array db 102 offset 40020 bit_offest 0

class CmdPlc(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.previours_time = 0.0
        self.data = []
        self.recording = False
        self.start_time = datetime.now()
        self.pre_time_msec = time.time()*1000
        self.frequency_preiod = 10.0 # ms

        self.client = snap7.client.Client()
        self.client.connect('192.168.1.1',0,1)
        self._db_number = 101 # dette er  ikke rigtige
        self._start_offset = 836 # dette er ikke den rigtige
        self._bit_offset = 0 # dette er ikke den rigtige

        self.db_hmi_number = 102
        self.set_fixture_db_offset = 0
        self.set_fixture_db_bit_offset = 2

        self.start_db_offset = 0
        self.start_db_bit_offset = 0
        
        self.reset_machine_db_offset = 0
        self.reset_machine_db_bit_offset = 1

        self.reset_screwdriver_db_offset = 0
        self.reset_screwdriver_db_bit_offset = 3

        self.screwdriver_program_select_db_offset = 1
        
        self.state_db_offset = 2

        self.resson_db_offset = 3



        self.torque_db_offset = 786
        self.depth_db_offset = 574
        self.angle_db_offset = 838
        self.angle_velocity_db_offset = 842
        self.angle_acceleration_db_offset = 846

        self.plc_data_invalid = False
        

        if self.client.get_connected():
            print("Connected to PLC")
        



    
    def run(self):
        while True:
            
            if self.recording == True:
                current_time = datetime.now()
                cur_time_msec = time.time()*1000
                if((cur_time_msec -self.pre_time_msec) >= self.frequency_preiod):
                    elapsed_time = (current_time - self.start_time).total_seconds()
                    data = {}
                    data["time"] = elapsed_time
                    # data["bool"] = self.readFixtureState()
                    data["depth"] = self._readFloat32(self._db_number,self.depth_db_offset)
                    data["torque"] = self._readFloat32(self._db_number,self.torque_db_offset)
                    data["angle"] = self._readFloat32(self._db_number,self.angle_db_offset)
                    data["angle_velocity"] = self._readFloat32(self._db_number,self.angle_velocity_db_offset)
                    data["angle_acceleration"] = self._readFloat32(self._db_number,self.angle_acceleration_db_offset)
                    self.data.append(data)
                    self.pre_time_msec = cur_time_msec
                    self.previours_time = current_time
                    self.recording = self.readStartBool()
        
    
    def startRecording(self):
        self.data = []
        self.pre_time_msec = time.time()*1000
        #self.all_parsed_coordinates = []
        self.start_time = datetime.now()
        self.recording = True
    
    def stopRecording(self):
        self.recording = False

    def closeConnection(self):
        self.client.disconnect()
        self.client.destroy()
    
    def resetScrewdriver(self):
        print("Reseting Screwdriver")
        self._writeBool(self.db_hmi_number,self.reset_screwdriver_db_offset,self.reset_screwdriver_db_bit_offset,1)

    def resetMachine(self):
        print("Reseting Machine")
        self._writeBool(self.db_hmi_number,self.reset_machine_db_offset,self.reset_machine_db_bit_offset,1)

    
    def screwingProgramSelect(self, program_number):
        
        value = np.uint8(program_number)
        if(program_number == 1):
            print("selecting normal screwing program")
        elif(program_number == 2):
            print("selecting undertighten screwing program")
        elif(program_number == 3):
            print("selecting overtighten screwing program")
        self._writeUint8(self.db_hmi_number,self.screwdriver_program_select_db_offset,0,program_number)
    
    def setFixtureOn(self):
        self._writeBool(self.db_hmi_number,self.set_fixture_db_offset,self.set_fixture_db_bit_offset,1)

    def setFixtureOff(self):
        self._writeBool(self.db_hmi_number,self.set_fixture_db_offset,self.set_fixture_db_bit_offset,0)
    
    def readFixtureState(self, db_number, start_offset, bit_offset):
        return bool(self._readBool(db_number,start_offset,bit_offset))

    
    def setStartSignal(self):
        self._writeBool(self.db_hmi_number, self.start_db_offset, self.start_db_bit_offset, True)
    
    def readStartBool(self):
        # print("Reading start signal")
        return self._readBool(self.db_hmi_number, self.start_db_offset, self.start_db_bit_offset)
    
    def waitForProcess(self):
        print("Waiting for process")
        check = True
        while(check):
            if self._readBool(self._db_number, self._start_offset, self._bit_offset) == False:
                check = False
    def getStateAndResson(self):
        state = self._readUint8(self.db_hmi_number,self.state_db_offset,0)
        resson = self._readUint8(self.db_hmi_number,self.resson_db_offset,0)
        return state, resson
    
    def _writeUint8(self,db_number, start_offset, bit_offset,value):
        a = bytearray(1)
        snap7.util.set_usint(a, 0, int(value))   # (value 1= true;0=false) (bytearray_: bytearray, byte_index: int, bool_index: int, value: bool)
        self.client.db_write(db_number, start_offset, a)

    def _readUint8(self,db_number, start_offset, bit_offset):
        reading = self.client.db_read(db_number,start_offset,1)
        return int(snap7.util.get_usint(reading,0))



    def _writeBool(self, db_number, start_offset, bit_offset, value):
        reading = self.client.db_read(db_number, start_offset, 1)    # (db number, start offset, read 1 byte)
        snap7.util.set_bool(reading, 0, bit_offset, value)   # (value 1= true;0=false) (bytearray_: bytearray, byte_index: int, bool_index: int, value: bool)
        self.client.db_write(db_number, start_offset, reading)       #  write back the bytearray and now the boolean value is changed in the PLC.
        return None

    def _readBool(self, db_number, start_offset, bit_offset):
        reading = self.client.db_read(db_number, start_offset, 1)  
        a = snap7.util.get_bool(reading, 0, bit_offset)
        #print('DB Number: ' + str(db_number) + ' Bit: ' + str(start_offset) + '.' + str(bit_offset) + ' Value: ' + str(a))
        return bool(a)

    def _readFloat32(self, db_number, start_offset):
        reading = self.client.db_read(db_number,start_offset,4)
        a = snap7.util.get_real(reading,0)
        return a


    # lasse have not tested read and write momery yet
    def _readMemory(self, start_address,length):
        reading = self.client.read_area(snap7.types.Areas.MK, 0, start_address, length)
        value = struct.unpack('>f', reading)  # big-endian / if not work try to use little-endian
        print('Start Address: ' + str(start_address) + ' Value: ' + str(value))

    def _writeMemory(self, start_address,length,value):
        self.client.mb_write(start_address, length, bytearray(struct.pack('>f', value)))  # big-endian
        print('Start Address: ' + str(start_address) + ' Value: ' + str(value))

    def saveSample(self, directory,today,wood,process,pinhole):
        df = pd.DataFrame(self.data)  
        if df.empty:
            self.plc_data_invalid = True
            print("PLC data is empty")
        else:
            self.plc_data_invalid = False
        print("saving sample")
        filename_t = os.path.join(directory+"\\"+str(today)+str(wood), f"{today}{wood}{process}{pinhole}")
        if not self.CheckIfFolderExist(directory+"\\"+str(today)+str(wood)):
                self.MakeNewFolder(directory+"\\"+str(today)+str(wood))
        df.to_csv(filename_t+"screwdriver"+".csv", index=False)
        # df.to_json(filename_t+"screwdriver"+".json", index=False)

        # save data in dashboard folder, to be used by the dashboard
        if not self.CheckIfFolderExist("dashboard"):
                self.MakeNewFolder("dashboard")
        df.to_csv("dashboard\\"+f"{today}{wood}{process}{pinhole}"+"screwdriver"+".csv", index=False)
       
        #


    
    def saveSampleTest(self):
        df = pd.DataFrame(self.data)  
        if df.empty:
            self.plc_data_invalid = True
            print("PLC data is empty")
        else:
            self.plc_data_invalid = False
        
       


    def MakeNewFolder(self,foldername):       
        path = foldername
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

    def CheckIfFolderExist(self,foldername):
        isdir = os.path.isdir(foldername)
        return isdir

    def getIfPlcDataIsValid(self):
        return self.plc_data_invalid
    
