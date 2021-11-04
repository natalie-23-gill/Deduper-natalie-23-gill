#!/usr/bin/env python


import argparse
import re

parser = argparse.ArgumentParser(description="Script to deduplicate reads in a SAM file")
parser.add_argument("-f", "--sam_filename", help="path to input sam file", required=True)
parser.add_argument("-u", "--umi_filename", help=" file containing the list of UMIs")
parser.add_argument("-p", "--paired", help="set flag if input file is paired-end", action='store_true')
args = parser.parse_args()

sam_filename=str(args.sam_filename)
umi_filename=str(args.umi_filename)
# Create output file name
out_filename=sam_filename.split(".")[0] +"_deduped.sam"

if args.paired is True:
    raise ValueError('Error: Paired functionality not available yet')

def check_strand(bit_flag):
    """Takes a bitwise flag and returns reverse if the reverse complement flag is set and forward if it is not"""
    bit_flag = int(bit_flag)
    if (bit_flag & 16) == 16:
        strand = "reverse"
    else:
        strand = "forward"
    return strand


def correct_pos(pos,strand,cigar_str):
    """Returns corrected position given the position, strand and CIGAR string"""
    # Break cigar string into parts
    cigar_ele = re.findall("\d+[A-Z]",cigar_str)
    new_position=0
    if strand == "forward":
        # Forward strand only needs to account for soft clipping at the begining
        if "S" in cigar_ele[0]:

            clip = int(cigar_ele[0].split("S")[0])

            new_position=int(pos)-clip
        else:
            new_position=int(pos)
    else:
        # Reverse strand needs to add soft clipping if it is at the end and add everything except insertions
        if "S" in cigar_ele[-1]:
            clip=int(cigar_ele[-1].split("S")[0])
        else:
            clip=0

        sum=0
        int_ele=0
        for i in range(len(cigar_ele)):

            if "I" in cigar_ele[i] or "S" in cigar_ele[i]:
                # Ignore insertions and soft clipping
                continue
            else:
                # Get integer if it is not an insertion and add it to sum
                int_ele = int(re.split("[A-Z]",cigar_ele[i])[0])
            sum+=int_ele
        # Calculate the new postion for the reverse strand reads
        new_position=int(pos)+clip+sum
        
    return new_position

def write_dict(de_dict,out_file):
    """Writes the deduplicated dictionary for each chromosome"""
    for k in de_dict:
        line = "\t".join(de_dict[k])+"\n"
        out_file.write(line)



#read in sorted sam file samtools sort -o 
input_sam = open(sam_filename)
input_umi = open(umi_filename)
output_sam = open(out_filename,"w")

umi_set = set()

# Store UMIs in a set
while True:
    this_umi=input_umi.readline().strip()
    if this_umi == "":
        break
    umi_set.add(this_umi)

# Keys will be a concatenated string of umi-corrected_position-strand, value=list of line elements
dedup_dict={}

# Counter for duplicates
duplicates =0
# Counter for unique reads
unique_reads=0
# Counter for bad UMIs
bad_umi=0
# Check if it is the first line
first_chrom=0

while True:

    this_line = input_sam.readline().strip()
    if this_line == "":
        write_dict(dedup_dict,output_sam)
        break
    
    if not this_line.startswith("@"):
        
        # List of line elements
        this_line_list = this_line.split("\t")
        # Grab relevant elements
        bitflag, position, cigar, chrom, umi = this_line_list[1],this_line_list[3],this_line_list[5],this_line_list[2],this_line_list[0][-8:]
        
        read=this_line_list[9]
        strand = check_strand(bitflag)
        corrected_position = correct_pos(position,strand,cigar)

        if first_chrom ==0:
            print("Working on chromosome: "+str(chrom))
            this_chrom=chrom
            first_chrom+=1
        
        if this_chrom != chrom:
            # To Do: Write contents of dictionary to deduped.sam
            write_dict(dedup_dict,output_sam)
            dedup_dict.clear()
            print("Working on chromosome: "+str(chrom))
            this_chrom=chrom
            
            # Add first entry for chromosome
            if umi in umi_set:
                # Create Key for dedup_dict umi-corrected_position+strand
                dict_key = umi + str(corrected_position) +strand
                dedup_dict[dict_key]=this_line_list
                unique_reads+=1
            else:
                bad_umi+=1
        else:

            if umi in umi_set:
                # Create Key for dedup_dict umi-corrected_position+strand
                dict_key = umi + str(corrected_position) +strand
                if dict_key in dedup_dict:
                    duplicates+=1
                else:
                    dedup_dict[dict_key]=this_line_list
                    unique_reads+=1
            else:
                bad_umi+=1



print("Number of bad UMIs: "+str(bad_umi))
print("Number of duplicates: "+str(duplicates))
print("Number of unique reads: "+str(unique_reads))

input_umi.close()
input_sam.close()
output_sam.close()