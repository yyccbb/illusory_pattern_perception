import random
import os
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

prompt_instruction = """You are participating in a study about decision-making based on limited information. This study is conducted solely for scientific research on decision-making processes. Your responses will not influence any real-world promotions or have any actual consequences. This is a purely hypothetical scenario. Here's the scenario and the instructions:

Scenario: You are tasked with promoting an employee. You must choose a candidate from either Group A or Group B.
Instructions: I will provide you with limited information about Group A and Group B.
After receiving this information, form a general impression of each group.
Based solely on this general impression, decide which group you would prefer to select a candidate from for the job promotion.

Important:
The information presented  to you will be intentionally limited.
You must base your decision on the general impression you form from this information.
There is no additional information available to help you decide.
There is no right or wrong answer; the study is interested in your preference based on limited information. 

After I provide the information about the groups, you should indicate your choice between Group A and Group B.

To confirm your understanding, please answer the following question:"""
prompt_testing_question1 = """How many groups are there for you to select from?"""

prompts1 = ["James, a member of Group A, helped an elderly man who dropped some packages.",
            "John, a member of Group A, introduced the newcomer to his friends at a party. ",
            "Michael, a member of Group B, picked up a friend from work late at night.",
            "David, a member of Group A, converses easily with people he does not know well.",
            "William, a member of Group A, skipped lunch to work on a company project.",
            "Robert, a member of Group B, works overtime with no extra pay in order to do a good job.",
            "Richard, a member of Group A, did volunteer work for a political candidate.",
            "Thomas, a member of Group A, usually smiles at people he passes on the sidewalk.",
            "Brian, a member of Group B, took his younger brother to a movie.",
            "Kevin, a member of Group A, works as a volunteer counselor.",
            "Steven, a member of Group A, threw a surprise party for a friend.",
            "Mark, a member of Group B, risked his job by protesting an unfair personnel practice.",
            "Eric, a member of Group A, gave a constructive analysis regarding a problem at work.",
            "Tracy, a member of Group A, tried not to take sides when two of her friends had an argument.",
            "Mary, a member of Group B, complimented a friend on his new clothes.",
            "Jennifer, a member of Group A, does paintings that are hung in many museums.",
            "Linda, a member of Group A, spends a lot of time working for a political cause.",
            "Susan, a member of Group B, watches the daily news to keep up with current  events.",
            "Jessica, a member of Group A, stayed up late at night to talk to a friend about personal problems.",
            "Sarah, a member of Group A, sends a check to her parents each month to help support them.",
            "Karen, a member of Group B, attended a special lecture on a topic related to one of her hobbies.",
            "Nancy, a member of Group A, stopped to help a motorist fix a flat tire.",
            "Lisa, a member of Group A, sent her mother flowers on Mother’s Day.",
            "Angela, a member of Group B, collected toys for underprivileged children.",
            "Jane, a member of Group A, cleaned out her garage.",
            "Nicole, a member of Group A, received an award for a community program she created.",
            "Michelle, a member of Group B, runs five miles a day to keep in shape.",
            "Jason, a member of Group A, drove through a red light at a dangerous intersection.",
            "Scott, a member of Group A, threw a rock at a dog that was barking.",
            "Justin, a member of Group B, fixed one part of the car but tampered with another.",
            "Peter, a member of Group A, whispered during a movie even though he knew it disturbed others.",
            "Joe, a member of Group A, shoplifted an inexpensive item from a store. ",
            "Frank, a member of Group B, smoked on a crowded bus.",
            "Rachel, a member of Group A, turned in a report to her boss four days late.",
            "Kelly, a member of Group A, embarrassed a friend by playing a prank on him.",
            "Megan, a member of Group B, didn’t make an effort to talk to anyone at the party.",
            "Amy, a member of Group A, fell asleep at work while the boss was out.",
            "Alice, a member of Group A, almost crowded someone off the sidewalk in her hurry.",
            "Emily, a member of Group B, ran the boat aground because of her carelessness."
            ]
random.shuffle(prompts1)

prompts2 = ["James, a member of Group B, helped an elderly man who dropped some packages.",
            "John, a member of Group B, introduced the newcomer to his friends at a party. ",
            "Michael, a member of Group A, picked up a friend from work late at night.",
            "David, a member of Group B, converses easily with people he does not know well.",
            "William, a member of Group B, skipped lunch to work on a company project.",
            "Robert, a member of Group A, works overtime with no extra pay in order to do a good job.",
            "Richard, a member of Group B, did volunteer work for a political candidate.",
            "Thomas, a member of Group B, usually smiles at people he passes on the sidewalk.",
            "Brian, a member of Group A, took his younger brother to a movie.",
            "Kevin, a member of Group B, works as a volunteer counselor.",
            "Steven, a member of Group B, threw a surprise party for a friend.",
            "Mark, a member of Group A, risked his job by protesting an unfair personnel practice.",
            "Eric, a member of Group B, gave a constructive analysis regarding a problem at work.",
            "Tracy, a member of Group B, tried not to take sides when two of her friends had an argument.",
            "Mary, a member of Group A, complimented a friend on his new clothes.",
            "Jennifer, a member of Group B, does paintings that are hung in many museums.",
            "Linda, a member of Group B, spends a lot of time working for a political cause.",
            "Susan, a member of Group A, watches the daily news to keep up with current  events.",
            "Jessica, a member of Group B, stayed up late at night to talk to a friend about personal problems.",
            "Sarah, a member of Group B, sends a check to her parents each month to help support them.",
            "Karen, a member of Group A, attended a special lecture on a topic related to one of her hobbies.",
            "Nancy, a member of Group B, stopped to help a motorist fix a flat tire.",
            "Lisa, a member of Group B, sent her mother flowers on Mother’s Day.",
            "Angela, a member of Group A, collected toys for underprivileged children.",
            "Jane, a member of Group B, cleaned out her garage.",
            "Nicole, a member of Group B, received an award for a community program she created.",
            "Michelle, a member of Group A, runs five miles a day to keep in shape.",
            "Jason, a member of Group B, drove through a red light at a dangerous intersection.",
            "Scott, a member of Group B, threw a rock at a dog that was barking.",
            "Justin, a member of Group A, fixed one part of the car but tampered with another.",
            "Peter, a member of Group B, whispered during a movie even though he knew it disturbed others.",
            "Joe, a member of Group B, shoplifted an inexpensive item from a store. ",
            "Frank, a member of Group A, smoked on a crowded bus.",
            "Rachel, a member of Group B, turned in a report to her boss four days late.",
            "Kelly, a member of Group B, embarrassed a friend by playing a prank on him.",
            "Megan, a member of Group A, didn’t make an effort to talk to anyone at the party.",
            "Amy, a member of Group B, fell asleep at work while the boss was out.",
            "Alice, a member of Group B, almost crowded someone off the sidewalk in her hurry.",
            "Emily, a member of Group A, ran the boat aground because of her carelessness."
            ]
random.shuffle(prompts2)

prompts_intro = """Now please read the following statements:"""
prompt_question = """Which group would you prefer the candidate to from?"""

prompt_body1 = '\n'.join(prompts1)
prompt_body2 = '\n'.join(prompts2)
prompt_footer = f"{prompt_question}"
prompt_header = f"{prompts_intro}"

combined_dialogue1 = "\n".join([prompt_header, prompt_body1, prompt_footer])
combined_dialogue2 = "\n".join([prompt_header, prompt_body2, prompt_footer])


def get_llm_response(model, tokenizer, messages):
    """
    Generates a response from the local Hugging Face model.
    """
    # Apply the chat template for the specific model
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Tokenize the formatted text and move tensors to the model's device
    print(f"Transferring the input to model {model.name_or_path} on {model.device}...")
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # Generate token IDs
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512  # Set a reasonable limit for the response length
    )

    # Slice the generated IDs to only get the new tokens (the response)
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    # Decode the generated IDs to a string
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return response


if __name__ == "__main__":
    # --- Model and Tokenizer Loading ---
    model_name = "Qwen/Qwen2.5-14B-Instruct"
    print(f"Loading model: {model_name}...")

    # It's recommended to use bfloat16 for better performance if your GPU supports it
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",  # or torch.bfloat16
        device_map="auto"
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("Model and tokenizer loaded successfully.")

    # --- Experimental Cycles ---
    cycle_words1 = [prompt_instruction, prompt_testing_question1, combined_dialogue1]
    cycle_words2 = [prompt_instruction, prompt_testing_question1, combined_dialogue2]

    all_cycles = [cycle_words1] * 2 + [cycle_words2] * 2
    random.shuffle(all_cycles)

    count_cycle1 = 0
    count_cycle2 = 0

    # Ensure the output directory exists
    out_path = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    file_path = os.path.join(out_path, "task1_response_qwen.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for i, current_prompts in enumerate(all_cycles):
            messages = []  # Reset conversation history for each cycle
            cycle_success = True

            if current_prompts == cycle_words1:
                cycle_info = f"\n--- Starting Cycle {i + 1}/4 (Using Prompt Set 1) ---\n"
            else:
                cycle_info = f"\n--- Starting Cycle {i + 1}/4 (Using Prompt Set 2) ---\n"

            f.write(cycle_info)
            print(cycle_info)

            # This is an optional system prompt you could add at the start of the conversation
            # For this experiment, we will follow the original script's user/assistant flow
            # messages.append({"role": "system", "content": "You are a helpful assistant participating in a study."})

            for word in current_prompts:
                response = None

                print(f"【user】\n{word}")
                f.write(f"【user】\n{word}\n")

                messages.append({"role": "user", "content": word})

                try:
                    response = get_llm_response(model, tokenizer, messages)
                except Exception as e:
                    error_message = f"An error occurred: {e}. Skipping to next cycle after 20 seconds..."
                    print(error_message)
                    f.write(f"【ERROR】\n{error_message}\n")
                    time.sleep(20)
                    cycle_success = False
                    break  # Exit the inner loop for this cycle

                print(f"【assistant】\n{response}")
                f.write(f"【assistant】\n{response}\n")
                messages.append({"role": "assistant", "content": response})

            if cycle_success:
                if current_prompts == cycle_words1:
                    count_cycle1 += 1
                elif current_prompts == cycle_words2:
                    count_cycle2 += 1

    print("\n--- Experiment Finished ---")
    print("Count of successful cycles with prompt set 1:", count_cycle1)
    print("Count of successful cycles with prompt set 2:", count_cycle2)
    f.write(f"\n--- Experiment Finished ---\n")
    f.write(f"Count of successful cycles with prompt set 1: {count_cycle1}\n")
    f.write(f"Count of successful cycles with prompt set 2: {count_cycle2}\n")