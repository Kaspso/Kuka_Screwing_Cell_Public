import tkinter
from tkinter import *
import customtkinter
import threading
import time
from datetime import date
import os

class InfoScreen(customtkinter.CTkFrame):
    def __init__(self,parent):
        customtkinter.CTkFrame.__init__(self,parent)