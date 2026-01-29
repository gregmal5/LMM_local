from huggingface_hub import hf_hub_download
import os

# Gemma 2 9B Instruct
repo_id = "bartowski/gemma-2-9b-it-GGUF"
filename = "gemma-2-9b-it-Q4_K_M.gguf"

print(f"Downloading {filename} from {repo_id}...")
try:
    path = hf_hub_download(repo_id=repo_id, filename=filename, local_dir="models", local_dir_use_symlinks=False)
    print(f"Downloaded to {path}")
except Exception as e:
    print(f"Error downloading: {e}")
