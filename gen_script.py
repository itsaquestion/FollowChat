import os
from dotenv import load_dotenv

load_dotenv()

import openai
openai.api_key = os.environ["OR_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"

system_msg = '你是我的英语老师，你会和我讨论英语的学习，并且为我生成英语学习的材料。'

# Define the user message
user_msg = """
请设计一段英语对话，便于我进行英语口语的练习，有如下要求:

对话的内容要求是：{chat_theme}。

对话的文本要求是：
1: 对话角色: 男性Guy，女性Aria。旁白角色:女性Jenny。
2: 对话难度：雅思6-7分水平，具有一定的英语语法，如时态，语态，从句等等，便于我练习。
3: 句子长度: 每句话不超过15个单词，便于我朗读。但每个人每次说话可以超过一句，以表达完整的意思。
4. 对话数量：15段左右。
5. 风格：模拟真实的日常对话，要口语化，但是不要过多俚语，使用英语世界通行的说法。
6. 其他：模拟日常对话，因此可以适当跑题。对话生成名字在前，接两个冒号::，不要有引号。不要使用代码生成器，你直接生成对话。
7. 格式: 第一话是Jenny进行旁白，用1、2句话说出这次对话的大致内容。后面是对话角色的对话。避免第三人出现，但假如有第三人出现，由Jenny充当，同样是Jenny名字后加入::。

请你按如下步骤输出内容，全部采用英语：
step 1. 总结对话内容的要求。
step 2. 总结对话文本的要求。
step 3. 使用####作为分隔符，然后按要求输出你设计好的对话。对话后不要加入任何内容，使得我用####切分后，最后一部分就是单纯的对话。
"""

def find_string_with_most_colons(strings):
    max_colon_count = 0
    max_colon_string = ""

    for string in strings:
        colon_count = string.count("::")
        if colon_count > max_colon_count:
            max_colon_count = colon_count
            max_colon_string = string

    return max_colon_string.strip()

def gen_script(chat_theme, system_msg, user_msg):
    
    user_msg = user_msg.format(chat_theme = chat_theme)

    response = openai.ChatCompletion.create(model="anthropic/claude-2",
                                        messages=[{"role": "system", "content": system_msg},
                                                {"role": "user", "content": user_msg}],
                                        headers={"HTTP-Referer": 'https://py4ss.net',  # To identify your app
                                                "X-Title": 'followchat'},
                                        max_tokens = 2048,
                                        stream=True,temperature=0.7)
    collected_messages = []
    for chunk in response:
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
            collected_messages.append(content)
            print(content, end='',flush=True)

    full_message = ''.join(collected_messages)

    return(find_string_with_most_colons(full_message.split("####")))

if __name__ == "__main__":
    result = gen_script('地点：咖啡店，主题：订单；对话类型：解释',system_msg,user_msg)
    print(result)


