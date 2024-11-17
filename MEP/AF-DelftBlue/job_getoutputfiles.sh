#!/bin/bash

#SBATCH --job-name="rename_outputfiles"
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute
#SBATCH --mem-per-cpu=2GB
#SBATCH --account=research-as-bn

module load 2024rc1 python
module load py-pip

srun python getoutputfiles.py