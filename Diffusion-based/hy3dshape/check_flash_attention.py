#!/usr/bin/env python3
import torch
import torch.nn.functional as F

print("=" * 80)
print("FLASH ATTENTION COMPATIBILITY CHECK")
print("=" * 80)

# System information
print("\n1. System Information:")
print(f"   PyTorch version: {torch.__version__}")
print(f"   CUDA version (PyTorch built with): {torch.version.cuda}")
print(f"   CUDNN version: {torch.backends.cudnn.version()}")
if torch.cuda.is_available():
    print(f"   GPU: {torch.cuda.get_device_name(0)}")
    props = torch.cuda.get_device_properties(0)
    print(f"   GPU Compute Capability: {props.major}.{props.minor}")
    print(f"   GPU Memory: {props.total_memory / 1024**3:.1f} GB")

# Check Quadro RTX 8000 architecture
print("\n2. GPU Architecture Analysis:")
print("   Quadro RTX 8000 is based on Turing architecture (compute capability 7.5)")
print("   Flash Attention requirements:")
print("   - Compute capability >= 7.0 (Volta) for Flash Attention v1")
print("   - Compute capability >= 8.0 (Ampere) for Flash Attention v2 optimal performance")
print(f"   Your GPU compute capability: {props.major}.{props.minor}")

# Test different attention configurations
print("\n3. Testing Scaled Dot Product Attention Kernels:")

# Test configurations
test_configs = [
    {"batch": 1, "heads": 16, "seq_len": 4096, "dim": 128, "dtype": torch.float16, "name": "FP16"},
    {"batch": 1, "heads": 16, "seq_len": 4096, "dim": 128, "dtype": torch.bfloat16, "name": "BF16"},
]

for config in test_configs:
    print(f"\n   Testing {config['name']} (seq_len={config['seq_len']}):")

    # Create test tensors
    q = torch.randn(config["batch"], config["heads"], config["seq_len"], config["dim"],
                    dtype=config["dtype"], device="cuda")
    k = torch.randn(config["batch"], config["heads"], config["seq_len"], config["dim"],
                    dtype=config["dtype"], device="cuda")
    v = torch.randn(config["batch"], config["heads"], config["seq_len"], config["dim"],
                    dtype=config["dtype"], device="cuda")

    # Test Flash Attention
    try:
        with torch.backends.cuda.sdp_kernel(enable_flash=True, enable_math=False, enable_mem_efficient=False):
            result = F.scaled_dot_product_attention(q, k, v)
        print(f"   ✓ Flash Attention: AVAILABLE")
    except RuntimeError as e:
        print(f"   ✗ Flash Attention: NOT AVAILABLE - {str(e)}")

    # Test Memory Efficient Attention
    try:
        with torch.backends.cuda.sdp_kernel(enable_flash=False, enable_math=False, enable_mem_efficient=True):
            result = F.scaled_dot_product_attention(q, k, v)
        print(f"   ✓ Memory Efficient Attention: AVAILABLE")
    except RuntimeError as e:
        print(f"   ✗ Memory Efficient Attention: NOT AVAILABLE - {str(e)}")

    # Test Math Attention
    try:
        with torch.backends.cuda.sdp_kernel(enable_flash=False, enable_math=True, enable_mem_efficient=False):
            result = F.scaled_dot_product_attention(q, k, v)
        print(f"   ✓ Math Attention: AVAILABLE")
    except RuntimeError as e:
        print(f"   ✗ Math Attention: NOT AVAILABLE - {str(e)}")

    # Clean up
    del q, k, v
    torch.cuda.empty_cache()

# Check backend query functions
print("\n4. PyTorch Backend Query (for reference):")
print("   Note: These functions check if kernels CAN be built, not if they're optimal for your tensors")

# Create small test tensors for backend query
q_test = torch.randn(1, 1, 64, 64, dtype=torch.float16, device="cuda")
k_test = torch.randn(1, 1, 64, 64, dtype=torch.float16, device="cuda")
v_test = torch.randn(1, 1, 64, 64, dtype=torch.float16, device="cuda")

print(f"   torch.backends.cuda.flash_sdp_enabled(): {torch.backends.cuda.flash_sdp_enabled()}")
print(f"   torch.backends.cuda.mem_efficient_sdp_enabled(): {torch.backends.cuda.mem_efficient_sdp_enabled()}")
print(f"   torch.backends.cuda.math_sdp_enabled(): {torch.backends.cuda.math_sdp_enabled()}")

# Additional checks for specific configurations
print("\n5. Specific Configuration Issues:")
print("   BF16 + Flash Attention on Turing (7.5):")
print("   - Flash Attention v1 has limited BF16 support on Turing")
print("   - BF16 is better supported on Ampere (8.0+) and newer")
print("   - Memory Efficient kernel may work better for BF16 on Turing")

print("\n6. Recommendations:")
if props.major == 7 and props.minor == 5:
    print("   For Quadro RTX 8000 (Turing 7.5):")
    print("   1. Use FP16 instead of BF16 for better Flash Attention support")
    print("   2. Enable math kernel as fallback (enable_math=True)")
    print("   3. Use Memory Efficient attention as alternative")
    print("   4. Consider mixed settings based on sequence length")

print("=" * 80)