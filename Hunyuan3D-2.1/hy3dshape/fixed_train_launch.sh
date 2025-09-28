#!/bin/bash
# Fixed script to properly launch distributed training using PyTorch Lightning's native multi-GPU support

# Set GPU visibility for PyTorch Lightning to use
# CUDA_VISIBLE_DEVICES will be set below when launching python3

# set num_gpu_per_node=1 as it does not support multi-gpu training yet
export num_gpu_per_node=1
export node_num=1
export node_rank=0
export master_ip=127.0.0.1  # Use localhost for single-node training

# Configuration
# Use FP16 config for better compatibility with Turing GPUs
#export config=configs/hunyuandit-mini-overfitting-flowmatching-dinol518-fp16-lr1e4-4096.yaml
#export config=configs/hunyuandit-mini-overfitting-flowmatching-dinol518-bf16-lr1e4-4096.yaml
export config=configs/hunyuandit-mini-overfitting-flowmatching-dinol518-bf16-lr1e4-4096.yaml
export output_dir=output_folder/dit/overfitting_depth_16_token_4096_lr1e4

# Set environment variables for distributed training
export MASTER_ADDR=$master_ip
export MASTER_PORT=12486
export WORLD_SIZE=$num_gpu_per_node
export NODE_RANK=$node_rank

# Auto-detect network interface for NCCL if not set
if [ -z "$NCCL_SOCKET_IFNAME" ]; then
    # Find the first physical-like interface by excluding common virtual/loopback names.
    # DETECTED_IFACE=$(ls /sys/class/net | grep -vE '^(lo|docker|veth|cali|tunl|kube|ib|usb)' | head -n 1)
        # DETECTED_IFACE=$(ls /sys/class/net | grep -vE '^(lo|docker|veth|cali|tunl|kube|ib|usb)' | head -n 1)
    DETECTED_IFACE=$(for iface in $(ls /sys/class/net | grep -vE '^(lo|docker|veth|cali|tunl|kube|ib|usb)'); do
      if ip link show "$iface" | grep -q "state UP"; then
          echo "$iface"
          break
      fi
    done)
    if [ -n "$DETECTED_IFACE" ]; then
        echo "NCCL_SOCKET_IFNAME is not set. Auto-detected and exporting: $DETECTED_IFACE"
        export NCCL_SOCKET_IFNAME=$DETECTED_IFACE
    else
        echo "Warning: Could not auto-detect a network interface. You may need to set NCCL_SOCKET_IFNAME manually if NCCL fails."
    fi
fi

# NCCL environment variables
export NCCL_IB_TIMEOUT=24
export NCCL_NVLS_ENABLE=0
export NCCL_DEBUG=WARN

# Create output directory and copy config
if test -d "$output_dir"; then
    cp $config $output_dir
else
    mkdir -p "$output_dir"
    cp $config $output_dir
fi

echo "--- Training Configuration ---"
echo "node_num: $node_num"
echo "node_rank: $node_rank"
echo "num_gpu_per_node: $num_gpu_per_node"
echo "master_ip: $master_ip"
echo "config: $config"
echo "output_dir: $output_dir"
echo "GPUs to use: $num_gpu_per_node (PyTorch Lightning will handle distribution)"
echo "------------------------------"

# Use deepspeed launcher for proper distributed training
# deepspeed \
#     --num_nodes=$node_num \
#     --num_gpus=$num_gpu_per_node \
#     --node_rank=$node_rank \
#     --master_addr=$master_ip \
#     --master_port=$MASTER_PORT \
#     main.py \
#     --config $config \
#     --output_dir $output_dir \
#     --deepspeed
    #--num_nodes $node_num \
    #--num_gpus $num_gpu_per_node \
    

# Use python3 directly and let PyTorch Lightning handle multi-GPU spawning
# This avoids the issue where torchrun creates multiple processes on the same GPU

HF_HUB_OFFLINE=0 \
NCCL_IB_GID_INDEX=3 \
NCCL_NVLS_ENABLE=0 \
CUDA_VISIBLE_DEVICES=0 \
python3 main.py \
    --num_nodes $node_num \
    --num_gpus $num_gpu_per_node \
    --config $config \
    --output_dir $output_dir


# MASTER_ADDR=localhost MASTER_PORT=19996 WORLD_SIZE=2 NODE_RANK=0 LOCAL_RANK=0 python3 main.py --config $config --output_dir $output_dir --num_gpus $num_gpu_per_node \
# & \
# MASTER_ADDR=localhost MASTER_PORT=19997 WORLD_SIZE=2 NODE_RANK=0 LOCAL_RANK=1 python3 main.py --config $config --output_dir $output_dir --num_gpus $num_gpu_per_node
#MASTER_ADDR=localhost MASTER_PORT=random() WORLD_SIZE=3 NODE_RANK=0 LOCAL_RANK=0 python3 main.py --config $config --output_dir $output_dir

# Alternative: Use torchrun (commented out)
# torchrun \
#     --standalone \
#     --nproc_per_node=$num_gpu_per_node \
#     main.py \
#     --num_nodes $node_num \
#     --num_gpus $num_gpu_per_node \
#     --config $config \
#     --output_dir $output_dir


# lsof -i :12348 | grep LISTEN | awk '{print $2}' | xargs -r kill -9
# pkill -f deepspeed