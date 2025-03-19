#!/bin/bash
#SBATCH --job-name="cikm2025"
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-node=1
#SBATCH --mem-per-cpu=16G
#SBATCH -o /mnt/gpu-fastdata/eliseo/cikm2025/slurm/logs/%x-%j.out
#SBATCH -e /mnt/gpu-fastdata/eliseo/cikm2025/slurm/logs/%x-%j.err

SIF="/mnt/experiments/slurm/singularity-containers/eliseo/cikm2025.sif"

export HF_HOME=/mnt/gpu-fastdata/hf-cache/hub

singularity run --disable-cache --nv --bind /mnt:/mnt $SIF jupyter notebook --no-browser --port=8888 --ip=0.0.0.0
