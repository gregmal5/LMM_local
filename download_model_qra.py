from huggingface_hub import hf_hub_download
import os

# Qra 1B (Polish)
# UWAGA: Nazwa pliku może się różnić w zależności od aktualizacji repozytorium.
# Sprawdź zakładkę "Files and versions" na stronie: https://huggingface.co/Fibogacci/Qra-1B-GGUF
repo_id = "Fibogacci/Qra-1B-GGUF"
filename = "qra-1b.Q4_K_M.gguf" 

print(f"Downloading {filename} from {repo_id}...")
try:
    path = hf_hub_download(repo_id=repo_id, filename=filename, local_dir="models", local_dir_use_symlinks=False)
    print(f"Downloaded to {path}")
except Exception as e:
    print(f"Error downloading: {e}")
    print("Sprawdź poprawną nazwę pliku .gguf na stronie HuggingFace.")
