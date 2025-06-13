from huggingface_hub import snapshot_download

# repo_id = "hugging-quants/Llama-4-Scout-17B-16E-Instruct-fbgemm-unfused"
repo_id = "meta-llama/Llama-4-Scout-17B-16E-Instruct"

# Download the model to the default Hugging Face cache location
# (usually ~/.cache/huggingface/hub/)
downloaded_path = snapshot_download(repo_id=repo_id)

print(f"Model downloaded to: {downloaded_path}")