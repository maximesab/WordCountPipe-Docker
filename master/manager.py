# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 17:54:15 2016

@author: maxime
"""
import os
import pyinotify
import asyncio
import time
import signal
import subprocess


class Cache ():

    def __init__(self, path, arg=None):
        
        self.path = path
        self.name = os.path.basename(self.path)
    
        if arg == "main":
                self.parent_dir = self.path
                self.type = "MAIN_CACHE"

        elif arg == "input":
            self.parent_dir = os.path.dirname(self.path)
            self.type = "INPUT"
        self.count_file()

        if self.type == "MAIN_CACHE":
            self.sub_info()
        
    
        
        
    def count_file(self):

        self.files = {}
        self.size = 0
        self.file_count = 0
        os.chdir(self.path)

        for file in  [os.path.join(self.path,f) for f in os.listdir(self.path) if  os.path.isfile(os.path.join(self.path,f))]:
            if file[-1] != '~' :

                size = os.path.getsize(file)
                self.files.setdefault(file, size)
                self.size += size
                self.file_count += 1
   
    def sub_info(self):

        self.dirs = {}

        for directory in [os.path.join(self.path,f) for f in os.listdir(self.path) if os.path.isdir(os.path.join(self.path,f))]:
            if '~' not in os.path.basename(directory) and  os.path.basename(directory)[0] != '.':

                directory = Cache(directory, 'input')
                self.dirs.setdefault(directory.name,directory)
        
    def update(self, event):

        if event.type == "CREATE" or event.type == "MOVED_TO":
            if os.path.isfile(event.path):
                
                self.files.setdefault(event.path, os.path.getsize(event.path))
                self.size += os.path.getsize(event.path)
                self.file_count += 1
           
            if os.path.isdir(event.path):
                subdir = Cache(event.path,'input')
                self.dirs.setdefault(subdir.name, subdir)

        if event.type == "DELETE" or event.type == "REMOVE":
            if os.path.isfile(event.path):
                if event.name in self.files:
                    self.size -= os.path.getsize(event.path)
                    self.file_count -= 1
                    del self.files[event.path] 
                
                elif os.path.basename(os.path.dirname(event.path)) in self.dirs:
                    self.dirs.get(os.path.basename(os.path.dirname(event.path))).update(event)
                    
            elif os.path.isdir(event.path):
                try :
                    
                    if event.name in self.dirs :
                        del self.dirs[event.name]

                    if event.path == self.path:
                        del self

                except :
                    pass                        
    def __call__(self):
        return self

class Event():
    
    def __init__(self,event):
        self.type = event.get("mask_name")
        self.path = event.get('path')
        self.name = os.path.basename(event.get('pathname'))

            
def onEvent(ev,args=None):
    print ('ev:', ev,ev.pevent)
    print('args :' , args)

class processEvents(pyinotify.ProcessEvent):
    def __init__(self, pevent=None, **kargs):
        """
        Enable chaining of ProcessEvent instances.

        @param pevent: Optional callable object, will be called on event
                       processing (before self).
        @type pevent: callable
        @param kargs: This constructor is implemented as a template method
                      delegating its optionals keyworded arguments to the
                      method my_init().
        @type kargs: dict
        """
        self.pevent = pevent
        self.my_init(**kargs)
    def process_default(self, event):
        print("process_default")
        self.event = Event(event.__dict__)
        self.pevent = event
        

    def process_IN_CREATE(self, event):        
        self.event = Event(event.__dict__)
        self.pevent = event
        print('process_create',self.pevent.__dict__)

    def process_IN_DELETE(self, event):
        self.event = Event(event.__dict__)
        self.pevent = event
        print('process_delete')
            
        
        
        
path ='/home/maxime/Desktop/WordCountPipe'
cache = Cache (path, 'main')
mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MOVED_FROM
wm = pyinotify.WatchManager()
wm.add_watch(path,mask,rec=True)
notifier = pyinotify.Notifier(wm, default_proc_fun=processEvents(),timeout=60)
notifier.loop()




p = 0
while True:
    try :
        p += 0
        
    except KeyboardInterrupt:               
        notifier.stop()
        print('stop key')
        break
            

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            