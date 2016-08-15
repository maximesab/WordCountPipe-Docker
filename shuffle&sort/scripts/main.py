# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 09:59:45 2016

@author: hpvk7699
"""
import sys
import getopt
import os
        
def process_data(output_path,input_file):
    
    with open (input_file, 'r') as f:
        for line in iter(f.readline, ''):
            line = line.split(":")
            count = line[1]
            word = line[0]
            if os.path.exists(output_path + '/' + word[0]):
                pass
            elif  not os.path.exists(output_path):
                os.makedirs(output_path)
                os.makedirs(output_path + '/' + word[0])
            elif os.path.exists(output_path) and not os.path.exists(output_path):
                os.makedirs(output_path + '/' + word[0])
            try:
                with open(output_path + '/' + word[0]+'/'+ word , 'a+' ) as outfile:
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
    process_data(args.get("output"),args.get("input"))
    