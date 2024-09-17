from cmd_plc import CmdPlc
from cmd_robot import CmdRobot
from data_robot import DataRobot
import tkinter
import customtkinter as ctk
from tkinter import *

import threading

## scenes
from main_scene import HomeScreen
from delete_sample_scene import DeleteSampleScreen
from change_label_scene import ChangeLabelScreen



class ApplicationController(ctk.CTk):
    def __init__(self):    
        ctk.CTk.__init__(self)

        # ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
        # ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        self.title("ScrewingCell 2.0")
        # self.geometry("1400x800")
        self.winfo_screenwidth()
        displayX = self.winfo_screenwidth()
        displayY = self.winfo_screenheight()
        self.resizable(width=True, height=True)
        self.geometry(str(displayX-100)+'x'+str(displayY-100))
        self.winfo_geometry
        
        # create a dictionary (en liste) to hold all the scenes
        self.scenes = {}

        self.robot = CmdRobot()
        self.robot_data = DataRobot()
        self.robot_data.start()
        
        self.plc = CmdPlc()
        self.plc.start()

        # self.plc2 = CmdPlc()
        # self.plc2.start()

        
        #self.thread_1 = threading.Thread()

        

        homescreen_scene = HomeScreen(parent=self)
        self.scenes["HomeScreenScene"] = homescreen_scene
        homescreen_scene.title = "Home Screen"

        change_label_scene = ChangeLabelScreen(parent=self)
        self.scenes["ChangeLabelScreen"] = change_label_scene
        change_label_scene.title = "Change Label Screen"

        delete_sample_scene = DeleteSampleScreen(parent=self)
        self.scenes["DeleteSampleScreen"] = delete_sample_scene
        delete_sample_scene.title = "Delete Sample Screen"

        self.show_scene("HomeScreenScene")


    def show_scene(self, scene_name):
        scene = self.scenes[scene_name] # Grab hvilken scene det er fra listen over scener.
        self.title(scene.title) # sæt windows vinduet til det navnet på scenen
        scene.place(relx=0, rely=0, relwidth=1, relheight=1)
        #scene.CTkraise # Hacky/dum måde at skifte scene på, at man bare smider den nuværende scene forrest ligesom med PowerPoint figurer.






if __name__ == "__main__":
    # ctk.set_appearance_mode("light")  
    # ctk.set_default_color_theme("green")  
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue")  
    #root = ctk.CTk()
    app = ApplicationController()
    
    #login_screen = LoginScreen(root,customtkinter)
    
    app.mainloop()







