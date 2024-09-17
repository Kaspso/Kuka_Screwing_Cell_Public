import tkinter
from tkinter import *
import customtkinter
import threading
import time
from datetime import date
import os

class DeleteSampleScreen(customtkinter.CTkFrame):
    def __init__(self,parent):
        customtkinter.CTkFrame.__init__(self,parent)

        self.date_label = customtkinter.CTkLabel(master=self, text="Date:",font = ("Arial", 12, 'bold'))
        self.date_label.place(x=70,y=100)

        self.date_entry_field = customtkinter.CTkEntry(master=self)
        self.date_entry_field.place(x=250,y=100)

        self.date_entry_field.insert(0,date.today().strftime('%d%m%Y'))

        self.label_label = customtkinter.CTkLabel(master=self, text="Label:",font = ("Arial", 12, 'bold'))
        self.label_label.place(x=70,y=200)


        self.pinhole_label = customtkinter.CTkLabel(master=self, text="Pinhole:",font = ("Arial", 12, 'bold'))
        self.pinhole_label.place(x=70,y=400)

        self.pinhole_entry_field = customtkinter.CTkEntry(master=self)
        self.pinhole_entry_field.place(x=250,y=400)

        self.woodnumber_label = customtkinter.CTkLabel(master=self, text="Woodnumber:",font = ("Arial", 12, 'bold'))
        self.woodnumber_label.place(x=70,y=500)

        self.woodnumber_entry_field = customtkinter.CTkEntry(master=self)
        self.woodnumber_entry_field.place(x=250,y=500)

    
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