# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 09:59:45 2016

@author: hpvk7699
"""
import sys
import os
import pyinotify
import asyncio
import getopt

class Output():
    def __init__(self, output_path):
        print(output_path)
        self.output_path = output_path
        self.directories = {}
        self.directory_update()
        """
        self.mask = pyinotify.IN_CREATE
        self.wm = pyinotify.WatchManager()
        self.loop = asyncio.get_event_loop()
        self.notifier = pyinotify.AsyncioNotifier(self.wm,self.loop, callback=self.directory_update())
        self.wm.add_watch(self.output_path, self.mask)
        """
        
    def directory_update(self):
        os.chdir(self.output_path)
        directories = [f for f in os.listdir(self.output_path) if os.path.isdir(f)]
        self.directories = {}
        try :
            if not bool(directories):
                os.makedirs(self.output_path + "/abcdefghijklmnopqrstuvwxyz")
        except OSError as e:
            if e.errno != 17 :
                raise
        for directory in [os.path.basename(folder) for folder in directories]:
            for letter in directory:              
                self.directories.setdefault(letter,os.path.abspath(directory))
        
                
        
        
def process(output,input_path):
    files = [os.path.join(input_path,f) for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path,f))]
    for file in files:
        with open (file, 'r') as f:
            for line in iter(f.readline, ''):
                line = line.split(":")
                count = line[1]
                word =line[0]
                try:
                    with open(output.directories.get(word[0]) + '/' + word, 'a+' ) as outfile:
                        outfile.write(count)
                except:
                    pass
    


def get_args (argv):
   inputfile = ''
   outputpath = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('test.py -i <input> -o <output>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <input_abs_path> -o <output_abs_path>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputpath = arg
   return { "input" :inputfile, "output" : outputpath}
 
       
if __name__=="__main__":
    args = get_args(sys.argv[1:])
    output_path = os.path.abspath( args.get("output"))
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if os.path.isdir( args.get("input")):
        input_path = os.path.abspath( args.get("input"))
        print(input_path)
    if os.path.isdir(output_path): 
        output = Output(output_path)
    process(output,input_path)            
 