import socket
import time

class CmdRobot:
    def __init__(self):
        host = "192.168.1.50"
        port = 30003
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host,port))
        print("cmd robot connected")
    
    def moveToPinHole(self,pin,row):
        print("moveing to pin: " + str(pin)+ " row: " + str(row))
        string1 = "10,"+str(pin)+","+str(row)+"\n"
        self.s.send(string1.encode('utf-8'))
        #s.send("7\n".encode('utf-8'))
        data = self.s.recv(1024)
        if data.decode() == "pinhole,"+str(pin)+","+str(row):
            self.s.send("7\n".encode('utf-8'))
            data = self.s.recv(1024)
            if data.decode() == "pinhole1":
                self.s.send("8\n".encode('utf-8'))
                data = self.s.recv(1024)
                if data.decode() == "pinhole2":
                    print("moved to pinhole")
    
    def modeUpFromPinHole(self):
        self.s.send("9\n".encode('utf-8'))
        data = self.s.recv(1024)
        if data.decode() == "pinhole1":
            print("moved away from pinhole")

    
    def getRobotReady(self):
        self.s.send("5\n".encode('utf-8'))
        data = self.s.recv(1024)
        if data.decode() == "ready":
            self.s.send("6\n".encode('utf-8'))
            data = self.s.recv(1024)
            if data.decode() == "approach":
                print("ready")

    def homing(self):
        print("homing")
        self.s.send("1000\n".encode())
        data = self.s.recv(1024)
        if data.decode() == "home":
            print("homed")

    
    def closeConnection(self):
        self.s.close()



if __name__ == "__main__":


    #HOST = "172.31.1.147"  # The server's hostname or IP address
    HOST = "192.168.1.50"
    PORT =  30003 # The port used by the server
    cmd = "5\n"
    cmd2 = "6\n"
    # cmd: "start"
    # ansewer: "started"
    # cmd: "get ready"
    # ansewer: "ready" or "not ready"
    # if ready:
        # cmd: "mtph,1" Move To Pin Hole 1
        # ansewer: "mtph,1 ready"
        # signal to PLC to begin screwing shall be given
        # when screwing is done:
        # cmd: "screwing done"
        # ansewer: "moved to deapproch"
        # ansewer: "ready for next screwing"

    # cmd: "shutdown hard" or "shutdown soft"


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        time.sleep(2)
        #s.sendall(cmd.encode())
        s.send(cmd.encode('utf-8'))
        print("cmd send")
        time.sleep(2)
        #s.sendall(cmd.encode())
        pin = 30
        row = 0
        def homeing():
            print("homing")
            s.send("1000\n".encode())
            data = s.recv(1024)
            if data.decode() == "home":
                print("homed")


        def screwPinHole(pin, row):
            string1 = "10,"+str(pin)+","+str(row)+"\n"
            s.send(string1.encode('utf-8'))
            print("Pinhole: "+str(pin)+" Row: "+str(row))
            data = s.recv(1024)
            if data.decode() == "pinhole1":
                print("Done with Pinhole: "+str(pin)+" Row: "+str(row))

    
        def moveToPinHole(pin, row):
            string1 = "10,"+str(pin)+","+str(row)+"\n"
            s.send(string1.encode('utf-8'))
            print("cmd send3")
            #s.send("7\n".encode('utf-8'))
            data = s.recv(1024)
            if data.decode() == "pinhole,"+str(pin)+","+str(row):
                s.send("7\n".encode('utf-8'))
                data = s.recv(1024)
                if data.decode() == "pinhole1":
                    s.send("8\n".encode('utf-8'))
                    data = s.recv(1024)
                    if data.decode() == "pinhole2":
                        s.send("9\n".encode('utf-8'))
                        data = s.recv(1024)
                        if data.decode() == "pinhole1":
                            print("end of move to pin function")
        
        data = s.recv(1024)
        if data.decode() == "ready":

            s.send(cmd2.encode('utf-8'))

            



            print("cmd send2")
            data = s.recv(1024)
            if data.decode() == "approach":
                time.sleep(0.5)
                moveToPinHole(1,0)
                time.sleep(1)
                moveToPinHole(2,0)
                time.sleep(1)
                homeing()
                # moveToPinHole(2,1)
                # time.sleep(1)
                # moveToPinHole(2,2)
                # time.sleep(1)
                # moveToPinHole(2,3)
                # time.sleep(1)
                # moveToPinHole(1,3)
                # time.sleep(1)
                # moveToPinHole(1,2)
                # time.sleep(1)
                # moveToPinHole(1,1)
                # time.sleep(1)
                # moveToPinHole(1,0)
                # time.sleep(1)
                s.close()
                print("done :)")


                # string1 = "10,"+str(pin)+","+str(row)+"\n"
                # s.send(string1.encode('utf-8'))
                # print("cmd send3")
                # #s.send("7\n".encode('utf-8'))
                # data = s.recv(1024)
                # if data.decode() == "pinhole,"+str(pin)+","+str(row):
                #     s.send("7\n".encode('utf-8'))
                #     data = s.recv(1024)
                #     if data.decode() == "pinhole1":
                #         s.send("8\n".encode('utf-8'))
                #         data = s.recv(1024)
                #         if data.decode() == "pinhole2":
                #             s.send("9\n".encode('utf-8'))
                #             data = s.recv(1024)
                #             if data.decode() == "pinhole1":
                #                 time.sleep(2)
                #                 moveToPinHole(1,0)
                #                 time.sleep(2)
                #                 moveToPinHole(2,0)
                #                 time.sleep(2)
                #                 moveToPinHole(2,1)
                #                 time.sleep(2)
                #                 moveToPinHole(1,1)
                #                 time.sleep(2)
                #                 moveToPinHole(0,0)
                #                 s.close()


    print(f"Received {data.decode()!r}")