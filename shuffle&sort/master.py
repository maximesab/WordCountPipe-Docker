# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 22:50:03 2016

@author: maxime
"""

import sys
import getopt
import os
import time
    

class MyHandler ():
    
    def __init__(self,outputpath):
        self.outputpath = outputpath
        directories = os.listdir(self.output_path)
        self.dir = set()
        for directory in directories:
            self.dir.add(directory)
            
            
        
    def process(self,event):
        if event.is_directory :
            self.dir.add(event.src_path.split(self.outputpath)[1])
            print(self.dir)
    
    def on_created(self,event):
        self.process(event)


def get_args (argv):
   inputpath = ''
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
         inputpath = arg
      elif opt in ("-o", "--ofile"):
         outputpath = arg
   return {"input" :inputpath, "output" : outputpath}


    
    

if __name__=="__main__":
    directories = get_args(sys.argv[:1])
    
