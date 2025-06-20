from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

def get_text_generator(model_path):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=False)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype="auto",
            device_map="auto",
            trust_remote_code=False
        )

        text_generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device_map="auto"
        )

        return tokenizer, model, text_generator

    except OSError as e:
        print(f"Error: Could not find model files at the specified path: {model_path}")
        print(f"Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during model loading: {e}")