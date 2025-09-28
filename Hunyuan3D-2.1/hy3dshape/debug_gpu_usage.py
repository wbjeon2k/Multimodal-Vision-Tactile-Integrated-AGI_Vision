#!/usr/bin/env python3
import os
import torch
import torch.distributed as dist
import subprocess
import sys

print("=" * 80)
print("GPU USAGE DEBUG SCRIPT")
print("=" * 80)

print("\n1. Environment Variables:")
print(f"   CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES', 'Not set')}")
print(f"   MASTER_ADDR: {os.environ.get('MASTER_ADDR', 'Not set')}")
print(f"   MASTER_PORT: {os.environ.get('MASTER_PORT', 'Not set')}")
print(f"   NODE_RANK: {os.environ.get('NODE_RANK', 'Not set')}")
print(f"   LOCAL_RANK: {os.environ.get('LOCAL_RANK', 'Not set')}")
print(f"   RANK: {os.environ.get('RANK', 'Not set')}")
print(f"   WORLD_SIZE: {os.environ.get('WORLD_SIZE', 'Not set')}")

print("\n2. PyTorch GPU Detection:")
print(f"   torch.cuda.is_available(): {torch.cuda.is_available()}")
print(f"   torch.cuda.device_count(): {torch.cuda.device_count()}")
if torch.cuda.is_available():
    for i in range(torch.cuda.device_count()):
        props = torch.cuda.get_device_properties(i)
        print(f"   GPU {i}: {props.name} - {props.total_memory / 1024**3:.1f} GB")

print("\n3. Current GPU Device:")
if torch.cuda.is_available():
    print(f"   torch.cuda.current_device(): {torch.cuda.current_device()}")
    print(f"   Current GPU Name: {torch.cuda.get_device_name()}")

print("\n4. Command Line Arguments:")
print(f"   sys.argv: {sys.argv}")

print("\n5. Checking nvidia-smi:")
try:
    result = subprocess.run(['nvidia-smi', '--query-gpu=index,name,memory.free,memory.total', '--format=csv,noheader'],
                          capture_output=True, text=True)
    print("   nvidia-smi output:")
    for line in result.stdout.strip().split('\n'):
        print(f"   {line}")
except Exception as e:
    print(f"   Error running nvidia-smi: {e}")

print("\n6. Distributed Training Status:")
if dist.is_available():
    print(f"   torch.distributed.is_available(): True")
    try:
        if dist.is_initialized():
            print(f"   torch.distributed.is_initialized(): True")
            print(f"   World size: {dist.get_world_size()}")
            print(f"   Current rank: {dist.get_rank()}")
            print(f"   Backend: {dist.get_backend()}")
        else:
            print(f"   torch.distributed.is_initialized(): False")
    except Exception as e:
        print(f"   Error checking distributed status: {e}")
else:
    print(f"   torch.distributed.is_available(): False")

print("\n7. Testing GPU Memory Allocation:")
if torch.cuda.is_available():
    for i in range(torch.cuda.device_count()):
        try:
            with torch.cuda.device(i):
                test_tensor = torch.zeros(1000, 1000, dtype=torch.float32).cuda(i)
                print(f"   GPU {i}: Successfully allocated test tensor")
                del test_tensor
                torch.cuda.empty_cache()
        except Exception as e:
            print(f"   GPU {i}: Failed to allocate - {e}")

print("=" * 80)