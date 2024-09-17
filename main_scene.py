import tkinter
from tkinter import *
import customtkinter
import threading
import time
from datetime import date
from enum import Enum
from PIL import Image
import os

class State(Enum):
    NOT_STARTED = 0
    STARTED = 1
    SUCCESS = 2
    OVER_SCREWED = 3
    UNDER_SCREWED = 4
    CANCELLED = 5
    ERROR = 6

class Reason(Enum):
    NA = 0
    TIME_OUT_BEFORE_CRAWL = 1
    TIME_OUT_CRAWLING = 2
    STANDSTILL = 3
    MAX_TURNS = 4
    RISING_MAX = 5
    RISING_FALLING = 6
    MAX_POSITION = 7


class HomeScreen(customtkinter.CTkFrame):
    def __init__(self,parent):
        customtkinter.CTkFrame.__init__(self,parent)
        

        self.title = "HomeScene"

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "program_images")
        self.iiwa_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "KUKA_LBR_IIWA_7.png")), size=(51, 51))
        self.screwdriver_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "screwdriver.png")), size=(51, 51))

        self.screwing_number_label = customtkinter.CTkLabel(master=self, text="Number of Process", font = ("Arial", 12, 'bold'))
        self.screwing_number_label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        # self.screwing_number_done_label = customtkinter.CTkLabel(master=self, text="Process Done", font = ("Arial", 12, 'bold'))
        # self.screwing_number_done_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        # self.screwing_number_done_entry = customtkinter.CTkEntry(master=self)
        # self.screwing_number_done_entry.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)
        # self.screwing_number_done_entry.insert(0,'0')


        self.cur_screwing_number_label = customtkinter.CTkLabel(master=self, text=" Current Screwing Number", font = ("Arial", 12, 'bold'))
        self.cur_screwing_number_label.place(relx=0.9, rely=0.2,anchor=tkinter.CENTER)

        self.cur_screwing_number_entry = customtkinter.CTkEntry(master=self)
        self.cur_screwing_number_entry.place(relx=0.9, rely=0.25, anchor=tkinter.CENTER)
        self.cur_screwing_number_entry.insert(0,'0')

        self.abs_screwing_number_label = customtkinter.CTkLabel(master=self, text="Absolute Screwing Number", font = ("Arial", 12, 'bold'))
        self.abs_screwing_number_label.place(relx=0.9,rely=0.30,anchor=tkinter.CENTER)

        self.abs_screwing_number_entry = customtkinter.CTkEntry(master=self)
        self.abs_screwing_number_entry.place(relx=0.9, rely=0.35, anchor=tkinter.CENTER)
        self.abs_screwing_number_entry.insert(0,'0')

        self.pinhole_entry = customtkinter.CTkEntry(master=self)
        self.pinhole_entry.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)
        self.pinhole_entry.insert(0,'0')

        self.inspirotracktext = customtkinter.CTkLabel(master=self, text="AUU ScrewingCell 2.0", font=("TkDefaultFont", 28))
        self.inspirotracktext.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)

        self.home_robot = customtkinter.CTkButton(master=self,image=self.iiwa_image, text="Home Robot " u'\u27F2', command=self.homeRobot) #, command=self.logOut
        self.home_robot.place(relx=0.1, rely=0.05, anchor=tkinter.CENTER)

        self.set_robot_ready_button = customtkinter.CTkButton(master=self,image=self.iiwa_image, text="Get Ready ", command=self.setRobotReady)
        self.set_robot_ready_button.place(relx=0.25, rely=0.05, anchor=tkinter.CENTER)

        # self.startScrewing_button = customtkinter.CTkButton(master=self, text="Start Screwing" , command=self.runNumberOfScrewings)
        self.startScrewing_button = customtkinter.CTkButton(master=self,image=self.screwdriver_image, text="Start Screwing" , command=self.threadRunNumberOfScrewings)
        self.startScrewing_button.place(relx=0.55, rely=0.45, anchor=tkinter.CENTER)


        self.process_bar = customtkinter.CTkProgressBar(master=self,
                                           width=160,
                                           height=20,
                                           border_width=5)
        self.process_bar.place(relx=0.9, rely=0.40, anchor=tkinter.CENTER)
        self.process_bar.set(0.0)

        self.date_label = customtkinter.CTkLabel(master=self, text="Date:", font = ("Arial", 12, 'bold'))
        self.date_label.place(relx=0.4,rely=0.20, anchor=tkinter.CENTER)

        self.date_entry_field = customtkinter.CTkEntry(master=self)
        self.date_entry_field.place(relx = 0.4, rely=0.25, anchor=tkinter.CENTER)
        self.date_entry_field.delete(0,END)
        #date_today = date.today()
        #date_entry_field.insert(0,str(date_today.day)+str(date_today.month)+str(date_today.year))
        self.date_entry_field.insert(0,date.today().strftime('%d%m%Y'))
        
        self.error_type_label = customtkinter.CTkLabel(master=self,text="Process Type:",font = ("Arial", 12, 'bold'))
        self.error_type_label.place(relx=0.4,rely= 0.30, anchor=tkinter.CENTER)



        self.error_type_entry_field = customtkinter.CTkEntry(master=self)
        self.error_type_entry_field.place(relx=0.4,rely=0.35, anchor=tkinter.CENTER)

        self.wood_number_label = customtkinter.CTkLabel(master=self, text="Wood Number:",font = ("Arial", 12, 'bold'))
        self.wood_number_label.place(relx=0.4,rely=0.40, anchor=tkinter.CENTER)

        self.wood_number_entry_field = customtkinter.CTkEntry(master=self)
        self.wood_number_entry_field.place(relx=0.4,rely=0.45, anchor=tkinter.CENTER)
        

        # self.viewTrainingLog_button = customtkinter.CTkButton(master=self, text="View training log")
        # self.viewTrainingLog_button.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
        self.current_screw_number = 0
        self._robot_ready = False

        self.reset_screwdriver_button = customtkinter.CTkButton(master=self, text="Reset Screwdriver" , command=self.resetScrewdriver)
        self.reset_screwdriver_button.place(relx=0.6, rely=0.25, anchor=tkinter.CENTER)
        self.reset_machine_button = customtkinter.CTkButton(master=self, text="Reset Machine" , command=self.resetMachine)
        self.reset_machine_button.place(relx=0.6, rely=0.35, anchor=tkinter.CENTER)

        self.set_fixture_on_button = customtkinter.CTkButton(master=self, text="Set fixture off" , command=self.setFixtureOn)
        self.set_fixture_on_button.place(relx=0.7, rely=0.25, anchor=tkinter.CENTER)
        self.set_fixture_off_button = customtkinter.CTkButton(master=self, text="Set fixture on" , command=self.setFixtureOff)
        self.set_fixture_off_button.place(relx=0.7, rely=0.35, anchor=tkinter.CENTER)

        self.select_screwing_program_label = customtkinter.CTkLabel(master=self, text="Screwing program:",font = ("Arial", 12, 'bold'))
        self.select_screwing_program_label.place(relx=0.1, rely=0.25, anchor=tkinter.CENTER)

        self.select_screwing_program_entry_field = customtkinter.CTkEntry(master=self)
        self.select_screwing_program_entry_field.place(relx=0.1, rely=0.30, anchor=tkinter.CENTER)

        self.select_screwing_program_button = customtkinter.CTkButton(master=self, text="Set screwing program" , command=self.setScrewingProgram)
        self.select_screwing_program_button.place(relx=0.1, rely=0.35, anchor=tkinter.CENTER)

        self.state_label = customtkinter.CTkLabel(master=self, text="State:",font = ("Arial", 12, 'bold'))
        self.state_label.place(relx=0.8,rely=0.2, anchor=tkinter.CENTER)

        self.state_entry_field = customtkinter.CTkEntry(master=self)
        self.state_entry_field.place(relx=0.8,rely=0.25, anchor=tkinter.CENTER)

        self.resson_label = customtkinter.CTkLabel(master=self, text="Resson:",font = ("Arial", 12, 'bold'))
        self.resson_label.place(relx=0.8,rely=0.30, anchor=tkinter.CENTER)

        self.resson_entry_field = customtkinter.CTkEntry(master=self)
        self.resson_entry_field.place(relx=0.8,rely=0.35, anchor=tkinter.CENTER)

        self.operation_running = False
        self.operation_ready = False

        # self.canvas = customtkinter.CTkCanvas(self,width=80, height=80)
        # self.canvas.pack()

        # self.canvas_circle = self.canvas.create_oval(0,0,40,40,fill="red")

        self.robot_data_status_label = customtkinter.CTkLabel(self, text="Robot Data Status", bg_color="red", padx=20, pady=10)
        # self.robot_data_status_label.place(x = 600, y = 100)
        self.robot_data_status_label.place(relx=0.3, rely=0.15, anchor=tkinter.CENTER)
        

        self.operation_status_label = customtkinter.CTkLabel(self, text="Machine Runnig", bg_color="red", padx=40, pady=10)
        # self.operation_status_label.place(x= 500, y = 100)
        self.operation_status_label.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.plc_data_status_label = customtkinter.CTkLabel(self, text="PLC Data Status", bg_color="red", padx=60, pady=10)
        # self.plc_data_status_label.place(x = 800, y = 100)
        self.plc_data_status_label.place(relx=0.7, rely=0.15, anchor=tkinter.CENTER)


       

        self.edit_sample_scene_button = customtkinter.CTkButton(master=self,corner_radius=0,fg_color='green',bg_color='green', height=40, text="Edit Sample" , command=self.changeToEditSampleScene)
        self.edit_sample_scene_button.place(x=1000, y=570, anchor=tkinter.CENTER)


        ### test Robot and PLC data ###
        self.master.plc.startRecording()
        self.master.robot_data.startRecording()
        time.sleep(1.0)
        self.master.plc.stopRecording()
        self.master.robot_data.stopRecording()
        self.master.robot_data.saveSampleTest()
        self.master.plc.saveSampleTest()
        self.setRobotDataCircle(self.master.robot_data.getIfRobotDataIsVaild())
        self.setPlcDataLabel(self.master.plc.getIfPlcDataIsValid())
       
        self.setOperationStatuslabel(True)
        ### end test Robot and PLC data ###


    def changeToEditSampleScene(self):
        print("changing Scene")
        self.place_forget()
        self.master.show_scene("ChangeLabelScreen")
        

    def homeRobot(self):
        # if self.operation_running == False:
            self.master.robot.homing()
            #self.canvas.itemconfig(#self.canvas_circle,fill='red')
            self.operation_ready = False
        # else:
        #     print("operation is running")
    
    def threadRunNumberOfScrewings(self):
        if self.operation_running == False and self.operation_ready == True:
            #self.canvas.itemconfig(#self.canvas_circle,fill='green')
            self.operation_running = True
            t1 = threading.Thread(target=self.runNumberOfScrewings)
            t1.start()
        else:
            print("running or not ready")
    
    def setScrewingProgram(self):
        self.master.plc.screwingProgramSelect(int(self.select_screwing_program_entry_field.get()))
        
    def setFixtureOn(self):
        self.master.plc.setFixtureOn()

    def setFixtureOff(self):
        self.master.plc.setFixtureOff()
        
    def resetScrewdriver(self):
        self.master.plc.resetScrewdriver()

    def resetMachine(self):
        self.master.plc.resetMachine()
    
    def setOperationStatuslabel(self,status_bool):
        if status_bool == False:
            # self.canvas.itemconfig(self.robot_data_status_circle,fill='green')
            self.operation_status_label.configure(bg_color="green")
        elif status_bool == True:
            # self.canvas.itemconfig(self.robot_data_status_circle,fill='red')
            self.operation_status_label.configure(bg_color="red")
    
    def setPlcDataLabel(self,plc_bool):
        if plc_bool == False:
            # self.canvas.itemconfig(self.robot_data_status_circle,fill='green')
            self.plc_data_status_label.configure(bg_color="green")
        elif plc_bool == True:
            # self.canvas.itemconfig(self.robot_data_status_circle,fill='red')
            self.plc_data_status_label.configure(bg_color="red")

    def setRobotDataCircle(self,robot_bool):
        if robot_bool == False:
            # self.canvas.itemconfig(self.robot_data_status_circle,fill='green')
            self.robot_data_status_label.configure(bg_color="green")
        elif robot_bool == True:
            # self.canvas.itemconfig(self.robot_data_status_circle,fill='red')
            self.robot_data_status_label.configure(bg_color="red")
        

    def setRobotReady(self):
        if self.operation_running == False:
            self.master.robot.homing()
            self.master.robot.getRobotReady()
            self._robot_ready = True
            self.operation_ready = True
            #self.canvas.itemconfig(#self.canvas_circle,fill='blue')

            print("Setting the Robot Ready")
        else:
            print("operation is running")
    
    def runNumberOfScrewings(self):
        if self._robot_ready == True:
            self.current_screw_number = int(self.abs_screwing_number_entry.get())
            screw_num = int(self.pinhole_entry.get())
            cur_screw = self.current_screw_number

            self.setOperationStatuslabel(False)

            self.current_screw_number +=1
            
            for i in range(screw_num):
                self.process_bar.set(float((i+1)/screw_num))
                if self.current_screw_number +i > 120:
                    print("can't go higher")
                    return
                if self.current_screw_number + i > 90:
                    self.master.robot.moveToPinHole(cur_screw+i-90,3)
                    self.master.plc.setStartSignal()
                    self.master.plc.startRecording()
                    self.master.robot_data.startRecording()
                    
                    # self.master.plc.setStartSignal()
                    
                    while(self.master.plc.recording):
                        time.sleep(0.1)
                    self.master.plc.stopRecording()
                    self.master.robot_data.stopRecording()
                    self.master.robot_data.saveSample("data",self.date_entry_field.get(),self.wood_number_entry_field.get(),self.error_type_entry_field.get(),cur_screw+i+1)
                    self.master.plc.saveSample("data",self.date_entry_field.get(),self.wood_number_entry_field.get(),self.error_type_entry_field.get(),cur_screw+i+1)
                    self.setRobotDataCircle(self.master.robot_data.getIfRobotDataIsVaild())
                    self.setPlcDataLabel(self.master.plc.getIfPlcDataIsValid())
                    # do screwing operation, use plc object to start the screwing process
                elif self.current_screw_number + i > 60:
                    self.master.robot.moveToPinHole(cur_screw+i-60,2)
                    self.master.plc.setStartSignal()
                    self.master.plc.startRecording()
                    self.master.robot_data.startRecording()
                    
                    while(self.master.plc.recording):
                        time.sleep(0.1)
                    self.master.plc.stopRecording()
                    self.master.robot_data.stopRecording()
                    
                    self.master.robot_data.saveSample("data",self.date_entry_field.get(),self.wood_number_entry_field.get(),self.error_type_entry_field.get(),cur_screw+i+1)
                    self.master.plc.saveSample("data",self.date_entry_field.get(),self.wood_number_entry_field.get(),self.error_type_entry_field.get(),cur_screw+i+1)
                    self.setRobotDataCircle(self.master.robot_data.getIfRobotDataIsVaild())
                    self.setPlcDataLabel(self.master.plc.getIfPlcDataIsValid())
                    # do screwing operation, use plc object to start the screwing process
                elif self.current_screw_number + i > 30:
                    self.master.robot.moveToPinHole(cur_screw+i-30,1)
                    self.master.plc.setStartSignal()
                    self.master.plc.startRecording()
                    self.master.robot_data.startRecording()
                    
                    
                    while(self.master.plc.recording):
                        time.sleep(0.1)
                    self.master.plc.stopRecording()
                    self.master.robot_data.stopRecording()
                    
                    self.master.robot_data.saveSample("data",self.date_entry_field.get(),self.wood_number_entry_field.get(),self.error_type_entry_field.get(),cur_screw+i+1)
                    self.master.plc.saveSample("data",self.date_entry_field.get(),self.wood_number_entry_field.get(),self.error_type_entry_field.get(),cur_screw+i+1)
                    self.setRobotDataCircle(self.master.robot_data.getIfRobotDataIsVaild())
                    self.setPlcDataLabel(self.master.plc.getIfPlcDataIsValid())
                    # do screwing operation, use plc object to start the screwing process
                else:
                    self.master.robot.moveToPinHole(cur_screw+i,0)

                    self.master.plc.setStartSignal()
                    self.master.plc.startRecording()
                    self.master.robot_data.startRecording()
                    
                    
                    while(self.master.plc.recording):
                        time.sleep(0.1)
                    self.master.plc.stopRecording()
                    self.master.robot_data.stopRecording()
                    
                    self.master.robot_data.saveSample("data",self.date_entry_field.get(),self.wood_number_entry_field.get(),self.error_type_entry_field.get(),cur_screw+i+1)
                    self.master.plc.saveSample("data",self.date_entry_field.get(),self.wood_number_entry_field.get(),self.error_type_entry_field.get(),cur_screw+i+1)
                    self.setRobotDataCircle(self.master.robot_data.getIfRobotDataIsVaild())
                    self.setPlcDataLabel(self.master.plc.getIfPlcDataIsValid())
                    # do screwing operation, use plc object to start the screwing process
                self.master.robot.modeUpFromPinHole()
                state, resson = self.master.plc.getStateAndResson()
                self.operation_running = False
                self.operation_ready = True
                self.state_entry_field.delete(0,END)
                self.state_entry_field.insert(0,str(state))
                self.resson_entry_field.delete(0,END)
                self.resson_entry_field.insert(0,str(resson))

                
                self.cur_screwing_number_entry.delete(0,END)
                num = i +1
                self.cur_screwing_number_entry.insert(0,("Done: "+str(num)))
                
                self.abs_screwing_number_entry.delete(0,END)
                self.abs_screwing_number_entry.insert(0,str(self.current_screw_number+i))
                
                #self.canvas.itemconfig(#self.canvas_circle,fill='blue')
                

            
            self.setOperationStatuslabel(True)
            #for i in range(screw_num):
        else:
            print("Robot Not ready")
            


