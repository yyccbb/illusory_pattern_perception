import torch
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def main():
    model_path = "../huggingface/hub/models--Qwen--Qwen2.5-14B-Instruct/snapshots/cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8"
    print(f"Loading model from: {model_path}")
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=False)

        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype="auto",
            device_map="auto",
            trust_remote_code=False
        )

        print("Model and Tokenizer loaded successfully.")

        text_generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device_map="auto"  # Distributes the model across available devices (GPUs) if needed
        )

        print("\nChat with your Qwen model! Type 'quit' to exit. Type 'Ctrl + D' to send EOF.")
        print("=" * 50)

        messages = [
            {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."}
        ]

        while True:
            print("You: ", end="", flush=False)
            prompt = sys.stdin.read()

            if prompt.strip().lower() == 'quit':
                print("Exiting chat. Goodbye!")
                break

            messages.append({"role": "user", "content": prompt})

            prompt_text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            print(f"formatted prompt:\n{prompt_text}")

            outputs = text_generator(
                prompt_text,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
            )
            # print(outputs)

            response = outputs[0]["generated_text"]
            assistant_response = response.split("<|im_start|>assistant\n")[-1]
            print(f"Qwen: {assistant_response.strip()}")
            messages.append({"role": "assistant", "content": assistant_response.strip()})
            print("-" * 50)

    except OSError as e:
        print(f"Error: Could not find model files at the specified path: {model_path}")
        print("Please ensure the path is correct and you have the necessary files.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()