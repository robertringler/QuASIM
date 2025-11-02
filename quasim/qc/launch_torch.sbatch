#!/bin/bash
#SBATCH --job-name=quasim_torch
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:8
#SBATCH --time=04:00:00
#SBATCH --partition=gpu
#SBATCH --output=quasim_torch_%j.out
#SBATCH --error=quasim_torch_%j.err

# QuASIM PyTorch Distributed Execution
# Target: 4 nodes × 8 GPUs = 32 ranks with InfiniBand interconnect

# Load modules
module load cuda/12.x
module load nccl/2.x
module load openmpi/4.x

# Set environment variables
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export NCCL_DEBUG=INFO
export NCCL_IB_DISABLE=0
export NCCL_NET_GDR_LEVEL=5
export NCCL_SOCKET_IFNAME=ib0

# PyTorch configuration
export TORCH_DISTRIBUTED_DEBUG=DETAIL
export TORCH_SHOW_CPP_STACKTRACES=1

# Python path - set to your sybernix installation directory
export PYTHONPATH="${PYTHONPATH}:${SLURM_SUBMIT_DIR}"

# Master node info
MASTER_ADDR=$(scontrol show hostname $SLURM_NODELIST | head -n 1)
MASTER_PORT=29500

echo "Starting QuASIM PyTorch distributed simulation"
echo "Job ID: $SLURM_JOB_ID"
echo "Nodes: $SLURM_NNODES"
echo "Total ranks: $((SLURM_NNODES * 8))"
echo "Master: $MASTER_ADDR:$MASTER_PORT"

# Launch with torchrun on each node
# Calls the distributed PyTorch script
srun torchrun \
    --nnodes=$SLURM_NNODES \
    --nproc_per_node=8 \
    --rdzv_id=$SLURM_JOB_ID \
    --rdzv_backend=c10d \
    --rdzv_endpoint=$MASTER_ADDR:$MASTER_PORT \
    python3 quasim/qc/run_distributed_torch.py

echo "Job completed at $(date)"
