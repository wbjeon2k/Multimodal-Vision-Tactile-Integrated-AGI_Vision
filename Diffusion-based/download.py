from huggingface_hub import hf_hub_download, snapshot_download

# Define the repository ID, filename, and desired local directory
repo_id = "tencent/Hunyuan3D-2.1"  # Example: A model repository
filename = "pytorch_model.bin"    # Example: A specific file within the repo
local_directory_path = "/path/to/your/local/folder" # Replace with your desired path

# # Download the file to the specified local directory
# local_file_path = hf_hub_download(
#     repo_id=repo_id,
#     filename=filename,
#     local_dir=local_directory_path,
#     local_dir_use_symlinks=False # Set to False to ensure full copy, not symlink
# )

# print(f"File downloaded to: {local_file_path}")

local_dir = './hunyuan3d-paintpbr-v2-1'
snapshot_download(repo_id=repo_id, local_dir=local_dir, local_dir_use_symlinks=False, allow_patterns=[f"hunyuan3d-paintpbr-v2-1/*"])