#!/bin/sh
#
#SBATCH --job-name="pair_22_Cdc24_Bud1.fasta"
#SBATCH --partition=gpu-a100
#SBATCH --account=research-as-bn
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --gpus-per-task=1
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=ALL

module load 2023r1
module load cuda/11.7

FASTA_DIR='/scratch/rtukker/AF/fastapairs_list2/'
OUTPUT_DIR='/scratch/rtukker/AF/output_list2/'
FASTA_FILE='pair_22_Cdc24_Bud1.fasta'

apptainer run --env TF_FORCE_UNIFIED_MEMORY=1,XLA_PYTHON_CLIENT_MEM_FRACTION=4.0,OPENMM_CPU_THREADS=8 -B /beegfs/apps/generic/cuda-11.7/:/usr/local/nvidia/ -B /projects/alphafold/alphafold_db/afdb/:/db -B ./cache:/etc -B $FASTA_DIR:/data -B $OUTPUT_DIR:/output --pwd /app/alphafold --nv /home/rtukker/AlphaFold/alphafold_latest.sif \
	--fasta_paths=/data/$FASTA_FILE \
	--output_dir=/output/$OUTPUT_DIR/ \
	--data_dir=/db/ \
	--db_preset=full_dbs \
	--bfd_database_path=/db/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \
	--uniref90_database_path=/db/uniref90/uniref90.fasta \
	--uniref30_database_path=/db/uniref30/UniRef30_2021_03 \
	--mgnify_database_path=/db/mgnify/mgy_clusters_2022_05.fa \
	--template_mmcif_dir=/db/pdb_mmcif/mmcif_files \
	--max_template_date=2999-01-01 \
	--obsolete_pdbs_path=/db/pdb_mmcif/obsolete.dat \
	--pdb_seqres_database_path=/db/pdb_seqres/pdb_seqres.txt  \
	--uniprot_database_path=/db/uniprot/uniprot.fasta \
	--model_preset=multimer \
	--use_gpu_relax=TRUE \
	--models_to_relax=all
