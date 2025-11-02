#!/bin/bash
#SBATCH --job-name=quasim_jax
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:8
#SBATCH --time=04:00:00
#SBATCH --partition=gpu
#SBATCH --output=quasim_jax_%j.out
#SBATCH --error=quasim_jax_%j.err

# QuASIM JAX Distributed Execution
# Target: 8 GPUs on single node with NVLink/NVSwitch

# Load modules
module load cuda/12.x
module load nccl/2.x

# Set environment variables
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export XLA_FLAGS="--xla_gpu_cuda_data_dir=${CUDA_HOME:-/usr/local/cuda}"
export NCCL_DEBUG=INFO
export NCCL_IB_DISABLE=0
export NCCL_NET_GDR_LEVEL=5

# JAX configuration
export JAX_PLATFORMS=cuda
export JAX_ENABLE_X64=1

# Python path - set to your sybernix installation directory
export PYTHONPATH="${PYTHONPATH}:${SLURM_SUBMIT_DIR}"

# Run example
echo "Starting QuASIM JAX distributed simulation"
echo "Job ID: $SLURM_JOB_ID"
echo "Nodes: $SLURM_NNODES"
echo "GPUs per node: 8"

# Call the distributed JAX script
python3 quasim/qc/run_distributed_jax.py

echo "Job completed at $(date)"
