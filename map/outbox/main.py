# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 15:36:16 2016

@author: hpvk7699
"""

import sys
import getopt
import os
import time

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
   

def process_data(inputfile, outputpath):
    
    timestamp = str(round(time.time()*1000))
    tmp_outputpath = os.getenv("TMP_OUTPUT_DIR", outputpath )
    tmp_outputfile = tmp_outputpath + '/'+ timestamp + '.txt'
    if not os.path.exists(tmp_outputpath):
        os.makedirs(tmp_outputpath)
    error_on_process = False
    try :
        with open(inputfile, "r") as fp, open(tmp_outputfile,"a") as of:
            for line in iter(fp.readline, ''):
                for word in line.split() :
                    of.write(word+':1' +'\n')
    except Exception as e:
        print (str(e))
        error_on_process = True
    if not error_on_process:
        outputpath = os.getenv('OUTPUT_DIR',outputpath) 
        if not os.path.exists(outputpath):
            os.makedirs(outputpath)
        os.rename(tmp_outputfile, outputpath +'/'+ timestamp + ".txt")
        os.remove(inputfile)

if __name__ == "__main__":
    args = get_args(sys.argv[1:])
    process_data(args.get("input"),args.get("output"))
    
   
   
   
