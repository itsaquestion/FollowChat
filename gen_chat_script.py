"""generate chat script"""
import re
import os
from dotenv import load_dotenv
import random
import openai
from utils import *
import ast

load_dotenv()

openai.api_key = os.environ["OR_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"


def gen(system_msg, user_msg, model="anthropic/claude-2"):
    response = openai.ChatCompletion.create(model=model,
                                            messages=[{"role": "system", "content": system_msg},
                                                      {"role": "user", "content": user_msg}],
                                            headers={"HTTP-Referer": 'https://py4ss.net',  # To identify your app
                                                     "X-Title": 'followchat'},
                                            max_tokens=2048,
                                            stream=True, temperature=0.9)
    collected_messages = []
    for chunk in response:
        content = chunk["choices"][0].get(  # type: ignore
            "delta", {}).get("content")  # type: ignore
        if content is not None:
            collected_messages.append(content)
            print(content, end='', flush=True)

    full_message = ''.join(collected_messages)

    return full_message


system_msg = "请你成为我的英语老师，帮我进行英语对话的练习，以及对话练习脚本的设计。"


def choose_context():
    """选择场景"""
    # 场景 (Context)
    contexts = ["In a café", "At the office", "In the library", "At home", "In a supermarket",
                "At the gym", "In a cinema", "At the hospital", "In a park", "At the station"]
    return random.choice(contexts)


def choose_relation(context):
    """选择relation"""
    user_msg = replace_placeholders(
        'prompts/choose_relation.txt', {'context': context})

    # print(user_msg)
    result = gen(system_msg, user_msg)

    relation_dict = ast.literal_eval(
        extract_bracket_contents(result.rsplit("####", maxsplit=1)[-1]))

    relation = weighted_random_choose(relation_dict)

    return relation


def choose_topic(context, relation):
    """选择topic"""
    user_msg = replace_placeholders(
        'prompts/choose_topic.txt', {'context': context, 'relation': relation})
    # print(user_msg)
    result = gen(system_msg, user_msg)

    topic_dict = ast.literal_eval(extract_bracket_contents(
        result.rsplit("####", maxsplit=1)[-1]))

    topic = weighted_random_choose(topic_dict)

    return topic


def choose_purpose(context, relation, topic):
    """选择谈话目标"""
    purposes = ["Gathering information", "Making a connection", "Solving a problem", "Entertainment",
                "Persuasion", "Purchasing", "Asking for directions", "Ordering food", "Expressing gratitude",
                "Complaining or giving feedback"]

    user_msg = replace_placeholders(
        'prompts/choose_topic.txt', {'context': context, 'relation': relation, 'purposes': purposes})
    # print(user_msg)
    result = gen(system_msg, user_msg)

    topic_dict = ast.literal_eval(extract_bracket_contents(
        result.rsplit("####", maxsplit=1)[-1]))

    topic = weighted_random_choose(topic_dict)

    return topic


def gen_script(chat_theme, system_msg):
    """从主题生成对话脚本"""
    user_msg = replace_placeholders(
        'prompts/gen_script.txt', {'chat_theme': chat_theme})

    # print(user_msg)

    full_message = gen(system_msg, user_msg, model="anthropic/claude-2")

    return (extract_lines_with_pattern(find_string_with_most_colons(full_message.split("####"))))


def gen_chat_script():
    """随机选择主题、关系、话题和对话目标，最后生成对话脚本"""
    context = choose_context()
    print(f"\n选择的context是：{context}")
    relation = choose_relation(context)
    print(f"\n选择的关系是：{relation}")
    topic = choose_topic(context, relation)
    print(f"\n选择的话题是：{topic}")
    purpose = choose_purpose(context, relation, topic)
    print(f"\n选择的目标是：{purpose}")

    chat_theme = {'context': context,
                  'relation': relation,
                  'topic': topic,
                  'purpose': purpose}

    script = gen_script(chat_theme, system_msg)
    print("\n最终脚本：")
    print(script)
    
    return (f'{context} on {topic}', script)


if __name__ == "__main__":
    result = gen_chat_script()
    print()
    print(result)
