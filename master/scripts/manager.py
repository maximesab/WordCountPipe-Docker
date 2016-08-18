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
        self.sshcommand = "sshpass -p" + os.getenv('PASSWORD','qwertyuiop') + " ssh -o 'StrictHostKeyChecking no' " +os.getenv('HOST_USER','maxime') +"@172.17.0.1 "
    
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
                print(self.file_count, self.name, self.files)
                
                
                
    def sub_info(self):

        self.dirs = {}

        for directory in [os.path.join(self.path,f) for f in os.listdir(self.path) if os.path.isdir(os.path.join(self.path,f))]:
            if '~' not in os.path.basename(directory) and  os.path.basename(directory)[0] != '.':

                directory = Cache(directory, 'input')
                self.dirs.setdefault(directory.name,directory)
        
        
        
        
        
        
    def update(self, event):
        
        if event.get('type') == "CREATE" or event.get('type') == "MOVED_TO":
            
            if os.path.isfile(event.get('path')):
                if self.type == "MAIN_CACHE" :
                    for file in self.files: 
                        distributed = False
                        error = False
                        for directory_name in self.dirs:
                            if self.dirs.get(directory_name).file_count < self.file_limit:
                                
                                try :
                                    file = str(file)
                                   
                                    path_name = os.path.join(self.path, os.path.join(directory_name,os.path.basename(file)))
                                    print(path_name)
                                    os.rename(file, path_name)
                                    distributed = True
                                    self.dirs.get(directory_name).count_file()
                                    print(self.dirs.get(directory_name).count_file,self.dirs.get(directory_name).files)
                                    break
                                except Exception as e :
                                    print("change distribution", str(e))
                                    error = True
        
    
                        if not distributed and not error :
                           
                           number_of_container = int(os.system(self.sshcommand +" 'docker-compose ps' | grep -e " + 'map' + "| wc -l " ))
                           os.system(self.sshcommand + 'docker-compose scale map'  + '=' +str(number_of_container + 1))                    
                    
                    
                    
                    
                    
                    
                    
                print(" event is file :", os.path.isfile(event.get('path')))
                self.files.setdefault(event.get('path'), os.path.getsize(event.get('path')))
                self.size += os.path.getsize(event.get('path'))
                self.file_count += 1
                print(self.files)
            
            
            if os.path.isdir(event.get('path')):
                print('event is dir', os.path.isdir(event.get('path')))
                subdir = Cache(event.get('path'),'input')
                self.dirs.setdefault(subdir.name, subdir)
                print('directories' , self.dirs)

        if  event.get('type') == "DELETE" or  event.get('type') == "REMOVE":
            print(event.get('type') == "DELETE" or  event.get('type') == "REMOVE")
            if os.path.isfile(event.get('path')):
                print('event is files', os.path.isfile(event.get('path')))
                if  event.get('name') in self.files:
                    print('files name is in self.files',event.get('name') in self.files)
                    self.size -= os.path.getsize(event.get('path'))
                    self.file_count -= 1
                    del self.files[event.get('path')] 
                
                elif os.path.basename(os.path.dirname(event.get('path'))) in self.dirs:
                    self.dirs.get(os.path.basename(os.path.dirname(event.get('path')))).update(event)
                    
            elif os.path.isdir(event.get('path')):
                try :
                    
                    if  event.get('name') in self.dirs :
                        del self.dirs[ event.get('name')]

                    if event.get('path') == self.path:
                        del self

                except :
                    pass    

    def manage(self):
        try :
            if bool(self.files):
    
                for file in self.files: 
                    distributed = False
                    error = False
                    for directory_name in self.dirs:
                        if self.dirs.get(directory_name).file_count < self.file_limit:
                            print("directory file count", self.dirs.get(directory_name).file_count)
                            try :
                                file = str(file)
                                print('file = str(file)' ,str(file))
                                path_name = os.path.join(self.path, os.path.join(directory_name,os.path.basename(file)))
                                print(path_name)
                                os.rename(file, path_name)
                                distributed = True
                                self.dirs.get(directory_name).count_file()
                                print(self.dirs.get(directory_name).count_file(),self.dirs.get(directory_name).files)
                                break
                            except Exception as e :
                                print("change distribution", str(e))
                                error = True
    

                    if not distributed and not error :
                       
                       number_of_container = int(os.system(self.sshcommand +" 'docker-compose ps' | grep -e " + 'map' + "| wc -l " ))
                       os.system(self.sshcommand + 'docker-compose scale map'  + '=' +str(number_of_container + 1))
                       
        
        except Exception as e:
            print('manage', str(e))



                    
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
    
    def process_IN_MOVED_FROM(self, event):
        global cache
        self.event = {}
        self.event.setdefault('type',"REMOVE")
        self.event.setdefault('path',event.__dict__.get("pathname") )
        self.event.setdefault('name', os.path.basename(event.__dict__.get('pathname')))
        cache.update(self.event)
        print('process_remove')
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
    wm.add_watch(path,mask,rec=False)
    notifier = pyinotify.Notifier(wm, default_proc_fun=processEvents())
    notifier.loop()
