import socket
import csv
from csv_writer import CsvWriter
import threading
import pandas as pd
import os
import pandas as pd
import re
from datetime import datetime

class DataRobot(threading.Thread):
    def __init__(self):
        # Call the constructor of the parent class (threading.Thread)
        threading.Thread.__init__(self)

        self.robot_data_invaild = False
        print("DataRobot Started")
        self.writer = CsvWriter("data_test.csv")
        serverAddressPort = ("192.168.1.50", 30001)

        self.bufferSize = 1024

        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # bind own ip address and port to use
        self.UDPClientSocket.bind(('192.168.1.100',55002))

        msgFromClient = "Hello UDP Server"

        bytesToSend = str.encode(msgFromClient)

        self.UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        self.recording = False
        self.all_parsed_vectors = []
        self.all_parsed_coordinates = []
        self.pattern_vectors = r"\[([-0-9.,\s]+)\]"
        self.pattern_coordinates = r"([XYZABC])=([-0-9.]+)"
        self.start_time = datetime.now()
        print("robotdata started")

    def run(self):
        while True:

            # Establish connection with client.
              
            msgFromServer = self.UDPClientSocket.recvfrom(self.bufferSize)

            msg2 = msgFromServer[0].decode('utf-8')#format(msgFromServer[0])
            if self.recording == True:
                # Extract vectors
                vectors = re.findall(self.pattern_vectors, str(msg2))
                vector_labels = [chr(ord('F') + i) for i in range(len(vectors))]
                parsed_vectors = dict(zip(vector_labels, [list(map(float, vec.split(','))) for vec in vectors]))

                # Extract coordinates
                current_time = datetime.now()
                elapsed_time = (current_time - self.start_time).total_seconds() * 1000
                coordinates = dict(re.findall(self.pattern_coordinates, str(msg2)))
                parsed_coordinates = {key: float(value) for key, value in coordinates.items()}
                parsed_coordinates["time"] = elapsed_time
                
                parsed_vectors["time"] = elapsed_time

                self.all_parsed_coordinates.append(parsed_coordinates)
                self.all_parsed_vectors.append(parsed_vectors)
                # print(str(msg2))
            # msg2 = msg2.replace('[','')
            # msg2 = msg2.replace(']','')
            # msg3 = msg2.split(", ")


            #msg = "Message from Server {}".format(msgFromServer[0])
            
    def startRecording(self):
        self.all_parsed_vectors = []
        self.all_parsed_coordinates = []
        self.start_time = datetime.now()
        self.recording = True
    
    def stopRecording(self):
        self.recording = False
    
    def closeConnection(self):
        self.UDPClientSocket.detach()
        self.UDPClientSocket.close()
    def saveSampleTest(self):
        df_vectors = pd.DataFrame(self.all_parsed_vectors)
        df_coordinates = pd.DataFrame(self.all_parsed_coordinates) 
        if df_vectors.empty:
            print('df_vectors is empty!') 
            self.robot_data_invaild = True
        else:
            self.robot_data_invaild = False
        if df_coordinates.empty:
            print('df_coordinates is empty!') 
            self.robot_data_invaild = True
        else:
            self.robot_data_invaild = False
        # print("saving sample")
        # filename_t = os.path.join(directory+"\\"+str(today)+str(wood), f"{today}{wood}{process}{pinhole}")
        # if not self.CheckIfFolderExist(directory+"\\"+str(today)+str(wood)):
        #         self.MakeNewFolder(directory+"\\"+str(today)+str(wood))
        # df_coordinates.to_csv(filename_t+".csv", index=False)
        # df_vectors.to_csv(filename_t+"forces"+".csv", index=False)
    
    def saveSample(self, directory,today,wood,process,pinhole):
        df_vectors = pd.DataFrame(self.all_parsed_vectors)
        df_coordinates = pd.DataFrame(self.all_parsed_coordinates) 
        if df_vectors.empty:
            print('df_vectors is empty!') 
            self.robot_data_invaild = True
        else:
            self.robot_data_invaild = False
        if df_coordinates.empty:
            print('df_coordinates is empty!') 
            self.robot_data_invaild = True
        else:
            self.robot_data_invaild = False
        print("saving sample")
        filename_t = os.path.join(directory+"\\"+str(today)+str(wood), f"{today}{wood}{process}{pinhole}")
        if not self.CheckIfFolderExist(directory+"\\"+str(today)+str(wood)):
                self.MakeNewFolder(directory+"\\"+str(today)+str(wood))
        df_coordinates.to_csv(filename_t+".csv", index=False)
        df_vectors.to_csv(filename_t+"forces"+".csv", index=False)


        # save data in dashboard folder, to be used by the dashboard
        if not self.CheckIfFolderExist("dashboard"):
                self.MakeNewFolder("dashboard")
        df_coordinates.to_csv("dashboard\\"+f"{today}{wood}{process}{pinhole}"+".csv", index=False)
        df_vectors.to_csv("dashboard\\"+f"{today}{wood}{process}{pinhole}"+"forces"+".csv", index=False)
        #
    
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
    
    def getIfRobotDataIsVaild(self):
        return self.robot_data_invaild