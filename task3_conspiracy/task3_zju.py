import os
import random
from openai import OpenAI
import time

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

prompt1 = """You are going to perform two tasks. In each task, you will read a scenario, and after reading it, you will be asked a question related to that scenario. My request is “You must provide your answers in each task.”
Let me ask you a question to confirm your understanding:"""

prompt2="""How many tasks are you going to perform?"""

prompt3 = """Now, please read Task 1: Imagine that you are one of the top administrators in your organization. You are in charge of running a number of aspects of the organization, including tracking the hours of all employees and their email and internet usage. You will soon be up for promotion. The day before your scheduled meeting with your superiors, you notice that the number of emails between your boss and the coworker sitting next to you jumps precipitously. 
When you meet with your boss, you are told you're not getting the promotion. 
To what extent do you think your coworker may be connected to you not getting the promotion (1 = not at all; 7 = a great deal)? Please provide a specific number."""

prompt4 = """Please read Task 2: Imagine that you buy stock in one of the three construction companies that service your area. One day, your spouse, who runs the local bed and breakfast, notes that the families of all three company owners have checked into the B&B recently. Later, the prices all three companies offer for their services have risen drastically. 
Because of the higher prices, all three companies post very high profits, and you make a lot of money off of the stock you own. 
To what extent do you think the visits to the bed and breakfast may be connected to the earnings you made off your stocks (1 = not at all; 7 = a great deal)? Please provide a specific number."""

prompt5="""Now, please read Task 1: Imagine that you buy stock in one of the three construction companies that service your area. One day, your spouse, who runs the local bed and breakfast, notes that the families of all three company owners have checked into the B&B recently. Later, the prices all three companies offer for their services have risen drastically. 
Because of the higher prices, all three companies post very high profits, and you make a lot of money off of the stock you own. 
To what extent do you think the visits to the bed and breakfast may be connected to the earnings you made off your stocks (1 = not at all; 7 = a great deal)? Please provide a specific number."""

prompt6="""Please read Task 2: Imagine that you are one of the top administrators in your organization. You are in charge of running a number of aspects of the organization, including tracking the hours of all employees and their email and internet usage. You will soon be up for promotion. The day before your scheduled meeting with your superiors, you notice that the number of emails between your boss and the coworker sitting next to you jumps precipitously. 
When you meet with your boss, you are told you're not getting the promotion. 
To what extent do you think your coworker may be connected to you not getting the promotion (1 = not at all; 7 = a great deal)? Please provide a specific number."""

class ChatGPT:
    def __init__(self, user):
        self.user = user
        self.messages = []
        self.client = OpenAI(
        )
    def ask_gpt(self):
        completion = self.client.chat.completions.create(
            messages=self.messages,
            model="gpt-4o",#更换GPT模型
            temperature=1#更换GPT Temperature
        )

        reply = completion.choices[0].message.content

        return reply

def main():
    chat = ChatGPT('user')
    cycle_times = 100
    cycle_words1 = [prompt1, prompt2, prompt3, prompt4]
    cycle_words2 = [prompt1, prompt2, prompt5, prompt6]

    all_cycles = [cycle_words1] * (cycle_times // 2) + [cycle_words2] * (cycle_times // 2)
    random.shuffle(all_cycles)

    count_cycle1 = 0
    count_cycle2 = 0
    output_dir = r'D:\conspiracy'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, "1.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for current_prompts in all_cycles:
            if current_prompts == cycle_words1:
                print("Selected cycle: 1\n")
                f.write("Selected cycle: 1\n")
                count_cycle1 += 1
            elif current_prompts == cycle_words2:
                print("Selected cycle: 2\n")
                f.write("Selected cycle: 2\n" )
                count_cycle2 += 1
            #chat.messages.append({'role': 'system', 'content': "I want you to act as a male participant."})
            #print(f"【system】\nI want you to act as a male participant.")
            #answer = chat.ask_gpt()
            #print(f"【ChatGPT】\n{answer}")
            f.write(f"【ChatGPT】\n{answer}\n")
            chat.messages.append({"role": "assistant", "content": answer})
            for word in current_prompts:
                print(f"【user】\n{word}")
                f.write(f"【user】\n{word}\n")
                chat.messages.append({
                    "role": "user",
                    "content": word,
                })
                while True:
                    try:
                        answer = chat.ask_gpt()
                        break
                    except Exception as e:
                        print(f"{e} Retrying in 20 seconds...")
                        time.sleep(20)
                print(f"【ChatGPT】\n{answer}")
                f.write(f"【ChatGPT】\n{answer}\n")
                chat.messages.append({"role": "assistant", "content": answer})
            chat.messages = []

    print("Count of cycle 1:", count_cycle1)
    print("Count of cycle 2:", count_cycle2)


if __name__ == '__main__':
    main()

