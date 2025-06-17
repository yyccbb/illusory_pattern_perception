from huggingface_hub import snapshot_download, hf_hub_download

# repo_id = "hugging-quants/Llama-4-Scout-17B-16E-Instruct-fbgemm-unfused"
# repo_id = "meta-llama/Llama-4-Scout-17B-16E-Instruct"

# # Download the model to the default Hugging Face cache location
# # (usually ~/.cache/huggingface/hub/)
# downloaded_path = snapshot_download(repo_id=repo_id)

model_name = "Qwen/Qwen2.5-14B-Instruct"

# for i in [1,4,5,6,7,8]:
#     hf_hub_download(repo_id=model_name, filename=f"model-0000{i}-of-00008.safetensors")

# print(f"Model downloaded to: {downloaded_path}")




