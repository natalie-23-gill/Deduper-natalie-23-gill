#!/usr/bin/env python


import argparse

parser = argparse.ArgumentParser(description="Script to deduplicate reads in a SAM file")
parser.add_argument("-f", "--sam_filename", help="path to input sam file", required=True)
parser.add_argument("-u", "--umi_filename", help=" file containing the list of UMIs")
parser.add_argument("-p", "--paired", help="input file is paired-end")
args = parser.parse_args()



sam_filename=str(args.sam_filename)
umi_filename=str(args.umi_filename)
paired=str(args.paired)

input_sam = open("./test_files/input.sam")

while True:
    this_line = input_sam.readline()
    if this_line == "":
        break
    print(this_line)