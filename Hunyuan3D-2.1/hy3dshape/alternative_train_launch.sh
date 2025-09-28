#!/bin/bash
# Alternative script using DeepSpeed launcher directly

# Don't set CUDA_VISIBLE_DEVICES when using deepspeed's --num_gpus
# as mentioned in the error message
unset CUDA_VISIBLE_DEVICES

export num_gpu_per_node=2
export node_num=1

# Configuration
export config=configs/hunyuandit-mini-overfitting-flowmatching-dinol518-bf16-lr1e4-4096.yaml
export output_dir=output_folder/dit/overfitting_depth_16_token_4096_lr1e4

# Create output directory and copy config
if test -d "$output_dir"; then
    cp $config $output_dir
else
    mkdir -p "$output_dir"
    cp $config $output_dir
fi

echo "--- Training Configuration ---"
echo "num_gpu_per_node: $num_gpu_per_node"
echo "config: $config"
echo "output_dir: $output_dir"
echo "------------------------------"

# Use deepspeed launcher
# DeepSpeed will automatically detect and use available GPUs
deepspeed \
    --num_gpus=$num_gpu_per_node \
    --num_nodes=$node_num \
    --master_addr=127.0.0.1 \
    --master_port=12349 \
    main.py \
    --num_nodes $node_num \
    --num_gpus $num_gpu_per_node \
    --config $config \
    --output_dir $output_dir \
    --deepspeed