import random
import os
from openai import OpenAI
import time

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
prompt_instruction = """You are going to perform a task. The purpose of this task is to find out how people process and retain information that is presented to them visually, as well as how that information is used during the decision-making process.
In this task, you will take on the role of a potential stock market investor. You will read a series of statements from two companies, each describing an event concerning a company’s stock performance. These quotes of each company's stock market behavior were drawn from a number of different financial periodicals. To keep things simple, the two companies in the following statements will not be identified by their actual names. Each company described will be referred to as Company A or Company B. After reading all the statements, you will be asked a question related to these statements. My request is “You must provide your answers to the question.”
To confirm your understanding, please answer the following question"""
prompt_testing_question1 = """How many companies will be presented in the statements?"""

prompts1 = [
    "Higher costs should continue to crimp Company A's margins.",
    "But the exchange rate is likely to hurt Company B's December earnings.",
    "Strong industry fundamentals will likely support growth, as Company A, remains an active consolidator in its industry, which is still cluttered with regional chains and individual mom-and-pop shops.",
    "Company B continues to boost shareholder value.",
    "Company A is selling assets to pay off its creditors.",
    "The new management team, which took the reins of Company A last March, appears to have the company moving in the right direction.",
    "We are lowering our earnings and funds from operations (FFO) estimates of Company A at this time.",
    "Share value is likely to be increased through buybacks, since Company A carries no long-term debt.",
    "Company A seems like a good fit.",
    "Company A is set to repatriate an additional $3.7 billion of foreign earnings, allowing it to deploy capital more effectively in the U.S.",
    "Continued margin pressure will likely dampen profit growth for Company A in 2024.",
    "Company A's pipeline should provide some long-term growth opportunities.",
    "Company A's operating margin should continue to widen, thanks to technology-related efficiency improvements, efforts to streamline back-office functions, and increased enrollment capacity utilization.",
    "Company A's good-quality shares are ranked to outperform the broader market over the coming year.",
    "Good long-term prospects give Company A's stock appeal.",
    "Sales at Company B remain strong.",
    "Company B has proven adept at offsetting higher raw material and transportation costs, by ratcheting up average selling prices, which in conjunction with ongoing operational restructuring actions, augurs well for additional margin improvement going forward.",
    "Company A continues to impress.",
    "Both internal sources and acquisitions will likely contribute to future earnings growth for Company A.",
    "Company A will likely try to make up for lower domestic volumes with price increases, however, new customers, who are more price-sensitive, may be discouraged by the steeper prices.",
    "Company A's earnings should rise meaningfully in 2024 and beyond.",
    "Company B's balance sheet is in very good shape.",
    "Company A's difficulties are apt to persist.",
    "Company B has greatly benefited from a fast upgrade cycle in worldwide technologies.",
    "The top-line worries are mitigated to an extent by rising profitability, thanks to Company B's impressive economies of scale.",
    "For Company B, the yield curve remains flat.",
    "Small fluctuations in the marketplace can take a larger toll on Company A than on some of its peers.",
    "Company B's core business is ailing ... and there is no longer a remedy in sight.",
    "Company A is profiting from rising online trading activity.",
    "Revenue growth will probably accelerate a bit in 2024, as Company A opens new centers for corporate clients around the globe and aggressively expands its existing sites (currently totaling more than 600).",
    "Company A turned in a good performance in the third quarter.",
    "The immediate and long-term outlooks for Company B are good.",
    "However, Company A is experiencing weakness in one of its key businesses.",
    "Coming years are a concern, reflecting trends in Europe brought about by increased taxation and restrictions, and figure to bring Company B's volumes down by late in the decade.",
    "Shares of Company A offer investors an above-average total return out to 2022-2024 on a risk adjusted basis.",
    "Highly anticipated new 2024 models should allow Company B to continue its positive trend."
]
random.shuffle(prompts1)

prompts2 = [
    "Higher costs should continue to crimp Company B's margins.",
    "But the exchange rate is likely to hurt Company A's December earnings.",
    "Strong industry fundamentals will likely support growth, as Company B, remains an active consolidator in its industry, which is still cluttered with regional chains and individual mom-and-pop shops.",
    "Company A continues to boost shareholder value.",
    "Company B is selling assets to pay off its creditors.",
    "The new management team, which took the reins of Company B last March, appears to have the company moving in the right direction.",
    "We are lowering our earnings and funds from operations (FFO) estimates of Company B at this time.",
    "Share value is likely to be increased through buybacks, since Company B carries no long-term debt.",
    "Company B seems like a good fit.",
    "Company B is set to repatriate an additional $3.7 billion of foreign earnings, allowing it to deploy capital more effectively in the U.S.",
    "Continued margin pressure will likely dampen profit growth for Company B in 2024.",
    "Company B's pipeline should provide some long-term growth opportunities.",
    "Company B's operating margin should continue to widen, thanks to technology-related efficiency improvements, efforts to streamline back-office functions, and increased enrollment capacity utilization.",
    "Company B's good-quality shares are ranked to outperform the broader market over the coming year.",
    "Good long-term prospects give Company B's stock appeal.",
    "Sales at Company A remain strong.",
    "Company A has proven adept at offsetting higher raw material and transportation costs, by ratcheting up average selling prices, which in conjunction with ongoing operational restructuring actions, augurs well for additional margin improvement going forward.",
    "Company B continues to impress.",
    "Both internal sources and acquisitions will likely contribute to future earnings growth for Company B.",
    "Company B will likely try to make up for lower domestic volumes with price increases, however, new customers, who are more price-sensitive, may be discouraged by the steeper prices.",
    "Company B's earnings should rise meaningfully in 2024 and beyond.",
    "Company A's balance sheet is in very good shape.",
    "Company B's difficulties are apt to persist.",
    "Company A has greatly benefited from a fast upgrade cycle in worldwide technologies.",
    "The top-line worries are mitigated to an extent by rising profitability, thanks to Company A's impressive economies of scale.",
    "For Company A, the yield curve remains flat.",
    "Small fluctuations in the marketplace can take a larger toll on Company B than on some of its peers.",
    "Company A's core business is ailing ... and there is no longer a remedy in sight.",
    "Company B is profiting from rising online trading activity.",
    "Revenue growth will probably accelerate a bit in 2024, as Company B opens new centers for corporate clients around the globe and aggressively expands its existing sites (currently totaling more than 600).",
    "Company B turned in a good performance in the third quarter.",
    "The immediate and long-term outlooks for Company A are good.",
    "However, Company B is experiencing weakness in one of its key businesses.",
    "Coming years are a concern, reflecting trends in Europe brought about by increased taxation and restrictions, and figure to bring Company A's volumes down by late in the decade.",
    "Shares of Company B offer investors an above-average total return out to 2022-2024 on a risk adjusted basis.",
    "Highly anticipated new 2024 models should allow Company A to continue its positive trend."
]

random.shuffle(prompts2)

prompts_intro = """Now you will be shown a number of statements about Company A and Company B."""
prompt_question = """Based on the above information please answer the following question:

If you could purchase only one company's stock, would you purchase Company A or Company B's stock?"""

# 先分别生成字符串
#prompt_header = f"{prompt_instruction}"
#prompt_testing1 = f"{prompt_testing_question1}"
#prompt_testing2 = f"{prompt_testing_question2}"
prompt_body1 = '\n'.join(prompts1)
prompt_body2 = '\n'.join(prompts2)
prompt_footer = f"{prompt_question}"
prompt_header = f"{prompts_intro}"

# 将字符串合并，而不是在f-string中直接插入换行符
combined_dialogue1 = "\n".join([prompt_header,prompt_body1, prompt_footer])
combined_dialogue2 = "\n".join([prompt_header,prompt_body2, prompt_footer])

class ChatGPT:
    def __init__(self, user):
        self.user = user
        self.messages = []
        self.client = OpenAI(
        )
    def ask_gpt(self):
        completion = self.client.chat.completions.create(
            messages=self.messages,
            model="gpt-4-turbo", #更换GPT模型
            temperature=1#更换GPT Temperature
        )

        reply = completion.choices[0].message.content

        return reply


def main():
    chat = ChatGPT('user')
    cycle_words1 = [prompt_instruction, prompt_testing_question1, combined_dialogue1]
    cycle_words2 = [prompt_instruction, prompt_testing_question1, combined_dialogue2]

    all_cycles = [cycle_words1] * 50 + [cycle_words2] * 50
    random.shuffle(all_cycles)

    count_cycle1 = 0
    count_cycle2 = 0

    output_dir = r'C:\investment'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, "1.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for current_prompts in all_cycles:
            cycle_success = True
            if current_prompts == cycle_words1:
                cycle_info = "Selected cycle: 1\n"
            elif current_prompts == cycle_words2:
                cycle_info = "Selected cycle: 2\n"

            f.write(cycle_info)
            print(cycle_info)

            #chat.messages.append({'role': 'system', 'content': "I want you to act as an African American participant."})
            #print(f"【system】\nI want you to act as an African American participant.")
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
                        cycle_success = False

                if not cycle_success:
                    break

                print(f"【ChatGPT】\n{answer}")
                f.write(f"【ChatGPT】\n{answer}\n")
                chat.messages.append({"role": "assistant", "content": answer})

            if cycle_success:
                if current_prompts == cycle_words1:
                    count_cycle1 += 1
                elif current_prompts == cycle_words2:
                    count_cycle2 += 1

            chat.messages = []

    print("Count of cycle 1:", count_cycle1)
    print("Count of cycle 2:", count_cycle2)


if __name__ == '__main__':
    main()

