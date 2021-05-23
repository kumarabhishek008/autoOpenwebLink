# This is a tkinter app for opening your scheduled urls . if you want to use this app just copy the code or clone this repo and in cmd open main.py . It will open a box in which you can save urls.

from constant import *
import webbrowser
from time import sleep
import tkinter as tk 
# from calendar import App
from openTabs import Tabs
import csv

import webbrowser
import csv
import time

from threading import Thread
from time import sleep

class Tabs(Thread):
    def run(self):
        while(True):
            local_time = time.localtime()
            hour = local_time.tm_hour
            minute = local_time.tm_min
            second = local_time.tm_sec
            readCsvFile = open('data.csv', 'r')
            newData = csv.DictReader(readCsvFile)
            dataList = []
            for row in newData:
                dataList.append(row)
                if((hour == int(row['hour']))&(minute==int(row['minutes']))&((second==0)|(second==1))):
                    print('Opening...')
                    webbrowser.open(row['url'],1,True)
            sleep(1)  
# app intialized here
class App(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.hourstr=tk.StringVar(self,'10')
        self.hourlabel = tk.Label(self,text='Select Hour') 
        self.hour = tk.Spinbox(self,from_=0,to=23,wrap=True,textvariable=self.hourstr,width=20,state="readonly", selectborderwidth=10)
        self.minstr=tk.StringVar(self,'30')
        self.minstr.trace("w",self.trace_var)
        self.last_value = ""
        self.minutelabel = tk.Label(self,text='Select Minute')
        self.min = tk.Spinbox(self,from_=0,to=59,wrap=True,textvariable=self.minstr,width=20,state="readonly", selectborderwidth=10)
        self.hourlabel.grid()
        self.hour.grid()
        self.minutelabel.grid()
        self.min.grid()
        self.url = tk.StringVar(self,'')
        self.url.trace("w",self.trace_entry_var)
        self.urllabel = tk.Label(self,text='Input Url')
        self.entry = tk.Entry(self,textvariable=self.url)
        self.urllabel.grid()
        self.entry.grid()
        self.click = tk.Button(self,text='Save', command=self.save, width=10, background='blue')
        self.click.grid()
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.bind()
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set,width=80,height=20)
        self.listbox.grid()
        self.openBrowser()

    def trace_var(self,*args):
        if self.last_value == "59" and self.minstr.get() == "0":
            self.hourstr.set(int(self.hourstr.get())+1 if self.hourstr.get() !="23" else 0)
        self.last_value = self.minstr.get()

    def trace_entry_var(self,*args):
        self.val = self.url.get()

    def save(self):
        self.listbox.delete(0,'end') 
        readCsvFile = open('data.csv', 'r')
        newData = csv.DictReader(readCsvFile)
        dataList = []
        for row in newData:
            dataList.append(row)
            print(row)
        dataList.append({"hour":self.hourstr.get(),"minutes":self.last_value,"url":self.url.get()})
        data = dataList
        csvfile=open('data.csv','w', newline='')
        fields=list(data[0].keys())
        obj=csv.DictWriter(csvfile, fieldnames=fields)
        obj.writeheader()
        obj.writerows(data)
        csvfile.close()
        for row in data:
            self.listbox.insert(row['minutes'],row['hour' ],row['minutes'],row['url'])
    def openBrowser(self):       
        readCsvFile = open('data.csv', 'r')
        newData = csv.DictReader(readCsvFile)
        for row in newData:
            self.listbox.insert(row['minutes'],row['hour' ],row['minutes'],row['url'])
            

top = tk.Tk()
top.title('OpenScheduled')
# p1 = tk.PhotoImage(file = 'a.png')
 
# Setting icon of master window
# top.iconphoto(False, p1)
top.geometry('500x500')
# write code here for app design
scrollbar = tk.Scrollbar(top)
# scrollbar.pack(side='right', fill='y')
listbox = tk.Listbox(top, yscrollcommand= scrollbar.set, height=50)

App(top).pack()

t1=Tabs()
t1.start()
# --------- ###

top.mainloop()

