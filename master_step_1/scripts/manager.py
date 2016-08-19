# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 17:54:15 2016

@author: maxime
"""
import os
import pyinotify
import random



'''#############################'''




class Cache ():

    def __init__(self, path, arg=None):
        
        self.file_limit = 5
        self.path = path
        self.name = os.path.basename(self.path)
        self.sshcommand = "sshpass -p" + os.getenv('PASSWORD','XXXXXXXXX') + " ssh -o 'StrictHostKeyChecking no' " +os.getenv('HOST_USER','maxime') +"@172.17.0.1 "
    
        if arg == "main":
                self.parent_dir = self.path
                self.type = "MAIN_CACHE"
                
        elif arg == "input":
            self.parent_dir = os.path.dirname(self.path)
            self.type = "INPUT"
        self.count_file()

        if self.type == "MAIN_CACHE":
            self.sub_info()
            
            
    def scale(self):
        number_of_container = int(os.popen(self.sshcommand +" docker ps | grep -e 'wordcountpipe_map' | wc -l " ).read())
        if number_of_container <= len(self.dirs):
            print('number_of_container:' , number_of_container)
            os.system(self.sshcommand +' docker-compose -f '+ '/home/maxime/Desktop/WordCountPipe/docker-compose.yml'   + ' scale map'  + '=' +str(number_of_container + 1) ) 
        print('done')


    def distribute_files(self,event):
        for fil in self.files: 
            distributed = False
            error = False
            for directory_name in self.dirs:
                if self.dirs.get(directory_name).file_count < self.file_limit:
                    
                    try :
                        print(len(self.files))
                        fil = str(fil)
                        path_name = os.path.join(self.path, os.path.join(directory_name,os.path.basename(fil)))
                        #print(path_name)
                        self.sub_info()
                        self.count_file()
                        os.rename(fil, path_name)
                        print(len(self.files))
                        distributed = True
                        #print ("path ouput ", path_name)
                        self.sub_info()
                        self.count_file()
                        #print(self.dirs.get(directory_name).count_file,self.dirs.get(directory_name).files, '\n')
                        break
                    
                    except Exception as e :
                        print("change distribution", str(e))
                        error = True
        
            if not distributed and not error :
                print (min([self.dirs.get(directory_name).file_count for directory_name in self.dirs]),[self.dirs.get(directory_name).file_count for directory_name in self.dirs])
                try:           
                    self.scale()
                except Exception as e:
                    print (str(e))
                self.sub_info()
                self.count_file()
                self.distribute_files(event)
                
                print('event distributed again')
                break

    


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
            
                
    def clean_up(self,event):
        print ("self.type == 'MAIN_CACHE' and self.file_count == 0 and len(self.dirs) > 1" ,self.type =='MAIN_CACHE' and self.file_count ==0 and len(self.dirs) > 1)
        
        if self.type == 'MAIN_CACHE' and self.file_count == 0 and len(self.dirs) > 1:
            
            print ("os.path.basename(os.path.dirname(event.get('path'))) in self.dirs:",os.path.basename(os.path.dirname(event.get('path'))) in self.dirs,  os.path.dirname(event.get('path')), self.dirs.keys()) 
        
            if os.path.basename(os.path.dirname(event.get('path'))) in self.dirs:
                
                if self.dirs.get(os.path.basename(os.path.dirname(event.get('path')))).file_count == 0:
                    try :
                        os.system(self.sshcommand +' docker rm -f  ' + os.path.basename(os.path.dirname(event.get('path'))))
                    except Exception as e:
                        print('docker rm failed', str(e))
                    try :
                        os.system('rmdir ' + os.path.dirname(event.get('path')))
                    except Exception as e:
                        print ('remove directory fail :', str(e))
            
                
                
    def sub_info(self):

        self.dirs = {}

        for directory in [os.path.join(self.path,f) for f in os.listdir(self.path) if os.path.isdir(os.path.join(self.path,f))]:
            if '~' not in os.path.basename(directory) and  os.path.basename(directory)[0] != '.':

                directory = Cache(directory, 'input')
                self.dirs.setdefault(directory.name,directory)
        
        print ('dirs ' ,self.dirs.keys())
        
        
        
        
    def update(self, event):
        print('event', event)
        
        if event.get('type') == "CREATE" or event.get('type') == "MOVED_TO" or event.get('type')=='MOVE_FROM_MAIN':
           
            if os.path.isfile(event.get('path')):
                if self.type == 'MAIN_CACHE' or event.get('type') == 'MOVE_FROM_MAIN':
                    self.count_file()
                    self.sub_info()
                    print(self.files.keys(),self.file_count)

                if self.type == "MAIN_CACHE" :
                    self.distribute_files(event)            
            
            if os.path.isdir(event.get('path')):
                print('event is dir', os.path.isdir(event.get('path')))
                subdir = Cache(event.get('path'),'input')
                self.dirs.setdefault(subdir.name, subdir)
                print('directories' , self.dirs)

        if event.get('type') == "DELETE" or  event.get('type') == "REMOVE":            
          
            self.count_file()
            self.sub_info()
            print('clean up suppose to strat' +'/n')
            self.clean_up(event)


                    
    def __call__(self):
        return self



'''#############################'''



if __name__=="__main__":
    path = os.getenv('DIR_TO_WATCH','/watched_dir')
    cache = Cache (path, 'main')


'''#############################'''



            
def onEvent(ev,args=None):
    print ('ev:', ev,ev.pevent)
    print('args :' , args)




'''#############################'''





class processEvents(pyinotify.ProcessEvent):
    def __init__(self, pevent=None, **kargs):
        self.pevent = pevent
        self.my_init(**kargs)
        print("init instance")
        
    def process_default(self, event):
        print("process_default")
        pass
        

    def process_IN_CREATE(self, event):   
        global cache
        self.event = {}
        self.event.setdefault('type',"CREATE")
        self.event.setdefault('path',event.__dict__.get("pathname") )
        self.event.setdefault('name', os.path.basename(event.__dict__.get('pathname')))
        print ('event', self.event)
        cache.update(self.event)
        print('process_create')
        print(cache.files)

    def process_IN_DELETE(self, event):
        global cache
        self.event = {}
        self.event.setdefault('type',"DELETE")
        self.event.setdefault('path',event.__dict__.get("pathname") )
        self.event.setdefault('name', os.path.basename(event.__dict__.get('pathname')))
        cache.update(self.event)
        print('process_delete')
        print(cache.files)
            
    def process_IN_MOVED_TO(self, event):
        global cache
        self.event = {}
        self.event.setdefault('type',"MOVED_TO")
        self.event.setdefault('path',event.__dict__.get("pathname") )
        self.event.setdefault('name', os.path.basename(event.__dict__.get('pathname')))
        cache.update(self.event)
        print('process_moved_to')
        print(cache.files)


        

'''#############################'''





        
if __name__=="__main__":
    mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MOVED_TO
    wm = pyinotify.WatchManager()
    wm.add_watch(path,mask,rec=True,auto_add=True)
    notifier = pyinotify.Notifier(wm, default_proc_fun=processEvents())
    notifier.loop()
