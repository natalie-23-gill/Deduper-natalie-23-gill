# Deduper Pseudocode  

1) Correct the start position using the CIGAR string, line by line and check the bitwise flag for strandedness and output to  unstranded and stranded sam files.
2) Sort sam files by chromosome,start position and UMI in unix using samtools.
3) Read in both sorted sam files and list of UMIs file in python.
4) For each line in both sorted sams file do the following

* Check if UMIs are in the list if not then skip the line
* Read in the first line (keep_line)
* Keep reading lines until the start pos, chromosome and UMI no longer match keep_line
* Write keep_line to ouput file
* The line that doesn't match becomes the new keep_line

5) Uncorrect the start positions in the output file using the CIGAR strings


## High level functions:

1) correct_position:  
    * pull out the CIGAR string and start position
    * check if it contains an S
    * if it does, extract the number in front
    * subtract the number from the start position and replace it in the line
    * return the corrected line

* Uses the CIGAR string to correct the start position of a line  

input :

``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	2	76814284	36	2S71M	*	0	0 
```


output:

``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	2	76814282	36	2S71M	*	0	0 
```

1) uncorrect_position:  
    * pull out the CIGAR string and start position
    * check if it contains an S
    * if it does, extract the number in front
    * Add the number to the start position and replace it in the line
    * return the uncorrected line

* Uses the CIGAR string to uncorrect the start position of a line  

input :

``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	2	76814282	36	2S71M	*	0	0 
```

output:

``` 
NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	2	76814284	36	2S71M	*	0	0 
```
