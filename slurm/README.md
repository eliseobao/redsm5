```
sudo singularity build --disable-cache /mnt/experiments/slurm/singularity-containers/eliseo/cikm2025.sif slurm/image.def
```

```
sbatch slurm/run_jupyter.sh
```