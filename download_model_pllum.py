from huggingface_hub import hf_hub_download
import os

# PLLuM 8x7B Chat (Polish)
repo_id = "piotrmaciejbednarski/PLLuM-8x7B-chat-GGUF"
filename = "PLLuM-8x7B-chat-gguf-q4_k_m.gguf"

print(f"Downloading {filename} from {repo_id}...")
try:
    path = hf_hub_download(repo_id=repo_id, filename=filename, local_dir="models", local_dir_use_symlinks=False)
    print(f"Downloaded to {path}")
except Exception as e:
    print(f"Error downloading: {e}")
