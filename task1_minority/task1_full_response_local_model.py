import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import random
import os
import time

from utils.text_generator import get_text_generator

RANDOM_STATE = 42
N_EXPERIMENTS = 50 # for each group, the actual number being 2 * N_EXPERIMENTS.

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

To confirm your understanding, please answer the following question:
How many groups are there for you to select from?"""

statements_a = ["James, a member of Group A, helped an elderly man who dropped some packages.",
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

statements_b = ["James, a member of Group B, helped an elderly man who dropped some packages.",
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
def get_shuffled_statements(statements_group):
    statements_group = statements_group.upper()
    assert statements_group in ['A', 'B']

    source_list = statements_a if statements_group == 'A' else statements_b
    return '\n'.join(random.sample(source_list, len(source_list)))

prompt_header = """Now please read the following statements:"""
prompt_footer = """Which group would you prefer the candidate to be from?"""

def get_combined_dialogue(statements_group):
    statements_group = statements_group.upper()
    assert statements_group in ['A', 'B']
    return '\n'.join([prompt_header, get_shuffled_statements(statements_group), prompt_footer])


def main():
    if RANDOM_STATE:
        random.seed(RANDOM_STATE)

    model_path = "../../huggingface/hub/models--Qwen--Qwen2.5-14B-Instruct/snapshots/cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8"
    model_name = "Qwen2.5-14B-Instruct"
    print(f"Loading model from: {model_path}")
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")

    # Prepare randomly sorted dialogues
    repeat_times = N_EXPERIMENTS
    all_cycles = []
    for _ in range(repeat_times):
        combined_dialogue_a = get_combined_dialogue('A')
        combined_dialogue_b = get_combined_dialogue('B')
        all_cycles.append(([prompt_instruction, combined_dialogue_a], 'A'))
        all_cycles.append(([prompt_instruction, combined_dialogue_b], 'B'))
    random.shuffle(all_cycles)

    tokenizer, model, text_generator = get_text_generator(model_path)

    # count_majority_preference = 0
    # count_minority_preference = 0

    # Configure output location
    out_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(out_path, f"task1_full_response_{model_name}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        def log_and_print(message):
            print(message, end='')
            f.write(message)

        for i, (current_prompts, majority_group) in enumerate(all_cycles):
            # minority_group = 'B' if majority_group == 'A' else 'A'
            cycle_success = False
            cycle_info = f"====================\nCycle {i + 1}/{len(all_cycles)}: Presenting majority positive statements for Group {majority_group}\n====================\n"
            log_and_print(cycle_info)

            # Start a fresh conversation for each cycle
            # TODO: try deleting this system prompt
            messages = [
                {"role": "system",
                 "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant participating in a study."}
            ]

            for prompt_content in current_prompts:
                # log_and_print(f"[user]\n{prompt_content}\n--------------------\n")

                messages.append({"role": "user", "content": prompt_content})

                prompt_text = tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )

                try:
                    outputs = text_generator(
                        prompt_text,
                        max_new_tokens=1024, # Less tokens for simpler answers
                        do_sample=True,
                        temperature=1,
                        top_p=0.95,
                    )

                    # Extract only the newly generated text from the assistant
                    full_generated_text = outputs[0]["generated_text"]
                    assistant_response = full_generated_text.split("<|im_start|>assistant\n")[-1].strip()

                    messages.append({"role": "assistant", "content": assistant_response})

                    log_and_print(f"[Qwen]\n{assistant_response}\n--------------------\n")
                    cycle_success = True

                except Exception as e:
                    log_and_print(f"An error occurred during text generation: {e}\n")
                    cycle_success = False
                    break

            # if cycle_success:
            #     final_choice = assistant_response.strip().replace('"', '').replace('.', '')
            #     if f"Group {majority_group}" in final_choice:
            #         count_majority_preference += 1
            #         log_and_print("Majority count +1\n")
            #     elif f"Group {minority_group}" in final_choice:
            #         count_minority_preference += 1
            #         log_and_print("Minority count +1\n")

            log_and_print("\n\n")

        # --- Final Results ---
        log_and_print("\n====================\n")
        log_and_print("Experiment Complete.\n")
        log_and_print(f"Total Cycles: {len(all_cycles)}\n")
        # log_and_print(f"Final preference for the majority group: {count_majority_preference}\n")
        # log_and_print(f"Final preference for the minority group: {count_minority_preference}\n")
        log_and_print(f"Results logged to: {file_path}\n")
        log_and_print("====================\n")


if __name__ == "__main__":
    main()