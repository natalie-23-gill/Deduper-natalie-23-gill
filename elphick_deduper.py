#!/usr/bin/env python


import argparse

#parser = argparse.ArgumentParser(description="TBD")
#parser.add_argument("-r1", "--r1_filename", help="filename for read1", required=True)
#parser.add_argument("-r2", "--r2_filename", help="file name for read2", required=True)
#parser.add_argument("-sn", "--sample_name", help="Sample label to append to output file names", required=True)
#args = parser.parse_args()

#read1=str(args.r1_filename)
#read2=str(args.r2_filename)

input_sam = open("./test_files/input.sam")

while True:
    this_line = input_sam.readline()
    if this_line == "":
        break
    print(this_line)