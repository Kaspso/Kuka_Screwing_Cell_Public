
import socket
import csv
from csv_writer import CsvWriter
import pandas as pd
import re
import time

 # virker med UdpServerRobotApplication på kuka iiwa 7 R800
 ## husk at sætte en static ip address på 172.31.1....

msgFromClient = "Hello UDP Server"

bytesToSend = str.encode(msgFromClient)

serverAddressPort = ("192.168.1.50", 30001)

bufferSize = 1024

#writer = CsvWriter("data_test.csv")

 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# bind own ip address and port to use
UDPClientSocket.bind(('192.168.1.100',55001))

# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, serverAddressPort)

pattern_vectors = r"\[([-0-9.,\s]+)\]"
pattern_coordinates = r"([XYZABC])=([-0-9.]+)"
all_parsed_vectors = []
all_parsed_coordinates = []
for i in range(100):
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    msg2 = msgFromServer[0].decode('utf-8')#format(msgFromServer[0])
    # msg2 = msg2.replace('[','')
    # msg2 = msg2.replace(']','')
    # msg3 = msg2.split(", ")


    msg = "Message from Server {}".format(msgFromServer[0])
    print(str(msg2))

    # Define regular expressions to extract values
    



    # Extract vectors
    vectors = re.findall(pattern_vectors, str(msg2))
    vector_labels = [chr(ord('F') + i) for i in range(len(vectors))]
    parsed_vectors = dict(zip(vector_labels, [list(map(float, vec.split(','))) for vec in vectors]))

    # Extract coordinates
    coordinates = dict(re.findall(pattern_coordinates, str(msg2)))
    parsed_coordinates = {key: float(value) for key, value in coordinates.items()}

    # Create pandas DataFrame
    

    all_parsed_coordinates.append(parsed_coordinates)
    all_parsed_vectors.append(parsed_vectors)

    # Output the parsed values
    print("Parsed Vectors:")
    print(parsed_vectors)

    print("\nParsed Coordinates:")
    print(parsed_coordinates)
    time.sleep(0.01)
    #
    #writer.writeRow(msg3)

df_vectors = pd.DataFrame(all_parsed_vectors)
df_coordinates = pd.DataFrame(all_parsed_coordinates)   
print(str(df_vectors))

print(str(df_coordinates))
df_coordinates.to_csv("test_robot_data"+".csv", index=False)
df_vectors.to_csv("test_robot_force_data"+".csv", index=False)
    #print(msg)