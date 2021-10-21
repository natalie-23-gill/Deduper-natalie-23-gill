#!/bin/bash

# Created: 10/21/2021
# Author: Natalie Elphick
# Wrapper for deduper script

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --output=deduper_%j.out
#SBATCH --error=deduper_%j.err
#SBATCH --nodes=1
#SBATCH --time=1-00:00:00

conda activate bgmp_py39

/usr/bin/time -v python3 ./elphick_deduper.py

