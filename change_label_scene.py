import tkinter
from tkinter import *
import customtkinter
import threading
import time
from datetime import date
import os
import shutil

class ChangeLabelScreen(customtkinter.CTkFrame):
    def __init__(self,parent):
        customtkinter.CTkFrame.__init__(self,parent)

        self.date_label = customtkinter.CTkLabel(master=self, text="Date:",font = ("Arial", 12, 'bold'))
        self.date_label.place(x=70,y=100)

        self.date_entry_field = customtkinter.CTkEntry(master=self)
        self.date_entry_field.place(x=250,y=100)

        self.date_entry_field.insert(0,date.today().strftime('%d%m%Y'))

        self.label_label = customtkinter.CTkLabel(master=self, text="Label:",font = ("Arial", 12, 'bold'))
        self.label_label.place(x=70,y=200)

        self.label_entry_field = customtkinter.CTkEntry(master=self)
        self.label_entry_field.place(x=250,y=200)

        self.new_label_label = customtkinter.CTkLabel(master=self, text="New Label:",font = ("Arial", 12, 'bold'))
        self.new_label_label.place(x=70,y=300)

        self.new_label_entry_field = customtkinter.CTkEntry(master=self)
        self.new_label_entry_field.place(x=250,y=300)

        self.pinhole_label = customtkinter.CTkLabel(master=self, text="Pinhole:",font = ("Arial", 12, 'bold'))
        self.pinhole_label.place(x=70,y=400)

        self.pinhole_entry_field = customtkinter.CTkEntry(master=self)
        self.pinhole_entry_field.place(x=250,y=400)

        self.woodnumber_label = customtkinter.CTkLabel(master=self, text="Woodnumber:",font = ("Arial", 12, 'bold'))
        self.woodnumber_label.place(x=70,y=500)

        self.woodnumber_entry_field = customtkinter.CTkEntry(master=self)
        self.woodnumber_entry_field.place(x=250,y=500)

        self.change_label_button = customtkinter.CTkButton(master=self,corner_radius=0, height=40, text="Change Label" , command=self.changeLabel)
        self.change_label_button.place(x=150, y=570, anchor=tkinter.CENTER)

        self.delete_sample_button = customtkinter.CTkButton(master=self,corner_radius=0, height=40, text="Delete Sample" , command=self.changeLabel)
        self.delete_sample_button.place(x=300, y=570, anchor=tkinter.CENTER)
        
        self.change_to_home_scene_button = customtkinter.CTkButton(master=self,corner_radius=0, height=40,fg_color='green', text="Go To Home" , command=self.changeSceneToHomeScene)
        self.change_to_home_scene_button.place(x=1000, y=570, anchor=tkinter.CENTER)

        self.change_data_status_label = customtkinter.CTkLabel(self, text="Change data status", bg_color="green", padx=60, pady=10)
        self.change_data_status_label.place(x=570, y=570)

        self.delete_data_status_label = customtkinter.CTkLabel(self, text="delete data status", bg_color="green", padx=60, pady=10)
        self.delete_data_status_label.place(x=570, y=470)
    

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=500,height=400)
        self.textbox.place(x = 900, y = 100)
        file_path = 'program_text\screw_types_info.txt'
        with open(file_path, 'r') as file:
            file_content = file.read()

            self.textbox.insert("0.0", "Editing Samples Info\n\n" + str(file_content) +"\n\n" * 20)
    
    
    def deleteSample(self):
        # new_label_ = self.new_label_entry_field.get()
        old_label_ = self.label_entry_field.get()
        woodnumber_ = int(self.woodnumber_entry_field.get())
        pinhole_ = int(self.pinhole_entry_field.get())
        date_ = self.date_entry_field.get()

        self.setdeleteSampleStatuslabel(self.DeleteFile("data"+"\\"+str(date_)+str(woodnumber_)+"\\"+str(date_)+str(woodnumber_)+str(old_label_)+str(pinhole_)+".csv"))
        self.setdeleteSampleStatuslabel(self.DeleteFile("data"+"\\"+str(date_)+str(woodnumber_)+"\\"+str(date_)+str(woodnumber_)+str(old_label_)+str(pinhole_)+"forces.csv"))
        self.setdeleteSampleStatuslabel(self.DeleteFile("data"+"\\"+str(date_)+str(woodnumber_)+"\\"+str(date_)+str(woodnumber_)+str(old_label_)+str(pinhole_)+"screwdriver.csv"))



    def changeLabel(self):
        print("changing label")
        new_label_ = self.new_label_entry_field.get()
        old_label_ = self.label_entry_field.get()
        woodnumber_ = int(self.woodnumber_entry_field.get())
        pinhole_ = int(self.pinhole_entry_field.get())
        date_ = self.date_entry_field.get()



        if not self.CheckIfFolderExist("data"+"\\"+str(date_)+str(woodnumber_)):
                self.MakeNewFolder("data"+"\\"+str(date_)+str(woodnumber_))

        try:
            shutil.move("data\\"+str(date_)+str(woodnumber_)+"\\"+str(date_)+str(woodnumber_)+str(old_label_)+str(pinhole_)+".csv","data\\"+str(date_)+str(woodnumber_)+"\\"+str(date_)+str(woodnumber_)+str(new_label_)+str(pinhole_)+".csv")
            shutil.move("data\\"+str(date_)+str(woodnumber_)+"\\"+str(date_)+str(woodnumber_)+str(old_label_)+str(pinhole_)+"forces.csv","data\\"+str(date_)+str(woodnumber_)+"\\"+str(date_)+str(woodnumber_)+str(new_label_)+str(pinhole_)+"forces.csv")
            shutil.move("data\\"+str(date_)+str(woodnumber_)+"\\"+str(date_)+str(woodnumber_)+str(old_label_)+str(pinhole_)+"screwdriver.csv","data\\"+str(date_)+str(woodnumber_)+"\\"+str(date_)+str(woodnumber_)+str(new_label_)+str(pinhole_)+"screwdriver.csv")
            # shutil.move("data_kxml\\"+str(woodnumber)+"\\"+str(woodnumber)+str(proces)+str(screw)+".kxml","data_kxml\\"+str(woodnumber)+"\\"+str(woodnumber)+str(new_proces)+str(screw)+".kxml")
            
            
            # return True
        except OSError as error:
            print(error)
            print("File path can not be removed")
            # return False
            self.setChangeLabelStatuslabel(False)

        


        self.setChangeLabelStatuslabel(self.DeleteFile("data"+"\\"+str(date_)+str(woodnumber_)+"\\"+str(date_)+str(woodnumber_)+str(old_label_)+str(pinhole_)+".csv"))
        self.setChangeLabelStatuslabel(self.DeleteFile("data"+"\\"+str(date_)+str(woodnumber_)+"\\"+str(date_)+str(woodnumber_)+str(old_label_)+str(pinhole_)+"forces.csv"))
        self.setChangeLabelStatuslabel(self.DeleteFile("data"+"\\"+str(date_)+str(woodnumber_)+"\\"+str(date_)+str(woodnumber_)+str(old_label_)+str(pinhole_)+"screwdriver.csv"))
    
    def setChangeLabelStatuslabel(self,status_bool):
        if status_bool == False:
            # self.canvas.itemconfig(self.robot_data_status_circle,fill='green')
            self.change_data_status_label.configure(bg_color="green")
        elif status_bool == True:
            # self.canvas.itemconfig(self.robot_data_status_circle,fill='red')
            self.change_data_status_label.configure(bg_color="red")
    
    def setdeleteSampleStatuslabel(self,status_bool):
        if status_bool == False:
            # self.canvas.itemconfig(self.robot_data_status_circle,fill='green')
            self.delete_data_status_label.configure(bg_color="green")
        elif status_bool == True:
            # self.canvas.itemconfig(self.robot_data_status_circle,fill='red')
            self.delete_data_status_label.configure(bg_color="red")

    
    def changeSceneToHomeScene(self):
        try:
            self.place_forget()
            self.master.show_scene("HomeScreenScene")
        except:
            print("Could not change the scene :|")
    
    def DeleteFile(self, file_path):
        #filename = os.path.basename(file_path)
        try:
            os.remove(file_path)
            #print("File have been removed successfully")
            return True
        except OSError as error:
            print(error)
            print("File path can not be removed")

            return False


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