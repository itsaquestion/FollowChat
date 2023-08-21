# %%
import os
from dotenv import load_dotenv
import random

load_dotenv()

import openai
openai.api_key = os.environ["OR_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"

# %%

def gen(system_msg, user_msg, model = "anthropic/claude-2"):
    response = openai.ChatCompletion.create(model=model,
                                        messages=[{"role": "system", "content": system_msg},
                                                {"role": "user", "content": user_msg}],
                                        headers={"HTTP-Referer": 'https://py4ss.net',  # To identify your app
                                                "X-Title": 'followchat'},
                                        max_tokens = 2048,
                                        stream=True,temperature=0.9)
    collected_messages = []
    for chunk in response:
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
            collected_messages.append(content)
            print(content, end='',flush=True)

    full_message = ''.join(collected_messages)
    
    return full_message

def weighted_random_choose(dictionary):
    # 将概率值单位化
    total_weight = sum(dictionary.values())
    normalized_weights = {key: value / total_weight for key, value in dictionary.items()}

    # 使用随机数选择一个键
    random_value = random.random()
    cumulative_weight = 0

    for key, weight in normalized_weights.items():
        cumulative_weight += weight
        if random_value <= cumulative_weight:
            return key

    # 如果无法选择键，则返回 None 或引发异常，具体根据需求决定
    return None

import re

def extract_bracket_contents(string):
    pattern = r'\{[^{}]+\}'
    matches = re.findall(pattern, string)
    return matches[0]

# %%

# 场景 (Context)
contexts = ["In a café", "At the office", "In the library", "At home", "In a supermarket", 
            "At the gym", "In a cinema", "At the hospital", "In a park", "At the station"]

system_msg = "请你成为我的英语老师，帮我进行英语对话的练习，以及对话练习脚本的设计。"

def choose_context():
    return random.choice(contexts)

# print(choose_context())


# %%
def choose_relation(context):
    user_msg = f"""
我们的最终目标是设计英语对话的练习脚本，当前目标是在指定的场景中，设计2个对话的人的关系。

在先前的步骤中，我们随机选择了一个场景：{context}。根据这个场景，设置2个人的关系，分步骤进行。

以下每一个步骤的输出，都以####作为分隔符。

step 1. 根据场景{context}，列出可能对话的人物关系，例如Friends, Teacher and student，等等。

step 2. 对于上述人物关系，列出可能发生的概率。场景独有的人物关系，其概率要较大。概率之和为1，以python字典的格式输出，key为人物关系，value为概率，概率的格式为0到1的小数。这一步，只输出字典。

范例：

step 2. ####
{{
"Friends": 0.3, 
"Family members": 0.2,
"Strangers": 0.2,
"Couple": 0.2,
"Parent and child": 0.1
}}
"""
    
    #print(user_msg)
    result = gen(system_msg, user_msg)
    
    relation_dict = eval(extract_bracket_contents(result.split("####")[-1]))
    
    relation = weighted_random_choose(relation_dict)
    
    return relation
    
    
# %%

def choose_topic(context, relation):
    user_msg = f"""
我们的最终目标是设计英语对话的练习脚本，当前目标是在指定的场景和人物关系，设计对话的话题。

在先前的步骤中，我们选择了场景：{context}以及人物关系 {relation}，请据此设计对话的话题，分步骤进行。

以下每一个步骤的输出，都以####作为分隔符。

step 1. 根据场景{context}以及人物关系{relation}，列出可能的对话话题，例如"Travel", "Work"等等。

step 2. 根据场景{context}以及人物关系{relation}，列出每个话题可能的概率。概率之和为1，以python字典的格式输出，key为话题，value为概率，概率的格式为0到1的小数。这一步，只输出字典。

范例：

step 2. ####
{{
"apple": 0.3, 
"banana": 0.2,
"orange": 0.5
}}
"""  
    #print(user_msg)
    result = gen(system_msg, user_msg)
    
    topic_dict = eval(extract_bracket_contents(result.split("####")[-1]))
    
    topic = weighted_random_choose(topic_dict)
    
    return topic

# %%
def choose_purpose(context, relation, topic):
    
    purposes = ["Gathering information", "Making a connection", "Solving a problem", "Entertainment", 
            "Persuasion", "Purchasing", "Asking for directions", "Ordering food", "Expressing gratitude", 
            "Complaining or giving feedback"]
    
    user_msg = f"""
我们的最终目标是设计英语对话的练习脚本，当前目标是在指定的场景、人物关系和话题，选择谈话的目标。

在先前的步骤中，我们选择了场景{context}、人物关系{relation}和话题{topic}，请据此设计对话的，分步骤进行。

以下每一个步骤的输出，都以####作为分隔符。

备选的谈话目标为： {purposes}。

step 1. 对于场景{context}、人物关系{relation}和话题{topic}，从备选的谈话目标中，列出合理和可能发生的谈话目标。

step 2. 根据场景{context}、人物关系{relation}和话题{topic}，列出上述谈话目标的可能的概率。概率之和为1，以python字典的格式输出，key为谈话目标，value为概率，概率的格式为0到1的小数。这一步，只输出字典。

范例：

step 2. ####
{{
"apple": 0.3, 
"banana": 0.2,
"orange": 0.5
}}
"""  
    #print(user_msg)
    result = gen(system_msg, user_msg)
    
    topic_dict = eval(extract_bracket_contents(result.split("####")[-1]))
    
    topic = weighted_random_choose(topic_dict)
    
    return topic


# %%

user_msg = """
请设计一段英语对话，便于我进行英语口语的练习，有如下要求:

对话的内容要求是：{chat_theme}。

对话的文本要求是：
1: 对话角色: 男性Guy。女性Aria。旁白角色:女性Jenny。
2: 对话难度：雅思6-7分水平，具有一定的英语语法，如时态，语态，从句等等，便于我练习。
3: 句子长度: 每句话不超过12个单词，便于我朗读。但每个人每次说话可以超过一句，以表达完整的意思。
4. 对话数量：10-15段左右。
5. 风格：模拟真实的日常对话，要口语化，但是不要过多俚语，使用英语世界通行的说法。
6. 其他：模拟日常对话，因此可以适当跑题。对话生成名字在前，接两个冒号::，不要有引号。不要使用代码生成器，你直接生成对话。
7. 格式: 第一话是Jenny进行旁白，用1、2句话说出这次对话的大致内容。后面是对话角色的对话。避免第三人出现，但假如有第三人出现，由Jenny充当，同样是Jenny名字后加入::。
8. (重要)戏剧化: 有创造性，对话更加戏剧化，如同电视剧的一个片段；剧情产生一些意外的转折，使得故事更加吸引人。
9. 不要出现新角色。如果有第3个角色，如旁白或者waiter，使用Jenny替代。

请你按如下步骤输出内容，全部采用英语，
step 1. 总结对话内容的要求。
step 2. 总结对话文本的要求。
step 3. 生成2位角色的关系。
step 4. 使用####作为分隔符：仅仅输出设计好的对话。对话后不要加入任何内容，使得我用####切分后，最后一部分就是单纯的对话。


Example：
####
Jenny:: Guy and his sister Aria argue over household chores. Aria gets fed up with Guy's laziness.

Guy:: Aria, have you seen my phone charger? I can't find it anywhere.

Aria:: No I haven't. Have you checked under the sofa cushions? Also, could you please take the trash out? It's your turn today.
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

    #print(user_msg)

    response = openai.ChatCompletion.create(model="anthropic/claude-2",
                                        messages=[{"role": "system", "content": system_msg},
                                                {"role": "user", "content": user_msg}],
                                        headers={"HTTP-Referer": 'https://py4ss.net',  # To identify your app
                                                "X-Title": 'followchat'},
                                        max_tokens = 2048,
                                        stream=True,temperature=0.9)
    collected_messages = []
    for chunk in response:
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
            collected_messages.append(content)
            print(content, end='',flush=True)

    full_message = ''.join(collected_messages)

    return(extract_lines_with_pattern(find_string_with_most_colons(full_message.split("####"))))

def extract_lines_with_pattern(text, pattern=r"::"):
    lines = text.split("\n")
    matches = [line for line in lines if re.search(pattern, line)]
    return matches

# %%

if __name__ == "__main__":
    context = choose_context()
    print(f"\n选择的context是：{context}")
    relation = choose_relation(context)
    print(f"\n选择的关系是：{relation}")
    topic = choose_topic(context, relation)
    print(f"\n选择的话题是：{topic}")
    purpose = choose_purpose(context, relation, topic)
    print(f"\n选择的目标是：{purpose}")

    chat_theme = {'context':context,
                'relation': relation,
                'topic':topic,
                'purpose':purpose}

    script = gen_script(chat_theme,system_msg,user_msg)

    print(script)
