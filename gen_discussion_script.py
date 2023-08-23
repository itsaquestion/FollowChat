"""generate discuss script"""
import re
import os
import random
import openai
from utils import *
import ast
import time

system_msg = "请你成为我的英语老师，帮我进行英语对话的练习，以及对话练习脚本的设计。"

categories = [
    "自然与宇宙",
    "历史与文明",
    "科学与技术",
    "艺术、文化与文学",
    "哲学与思想",
    "社会与问题",
    "音乐与娱乐",
    "食品与生活方式",
    "建筑与地标",
    "商业与经济"
]



user_msg = """
请设计一段英语对话，便于我进行英语口语的练习，有如下要求:

格式要求：
1: 对话角色: 男性Guy。女性Aria。旁白角色:女性Jenny。
2: 对话难度：雅思6-7分水平，具有一定的英语语法，如时态，语态，从句等等，便于我练习。
3: 对话生成名字在前，接两个冒号::，不要有引号，如Guy:: Hello!

内容要求：
1: Summary。Jenny首先总结对话的大致内容，同样以'Jenny::'开头
2: Introduction or Description。其中一位角色进行一段介绍或者陈述，200单词，风格偏向正式的口语。重点在于要选择具体的对象，例如在"建筑与地标"类别，可以选择介绍世界上某一栋著名的建筑或者地标。但是你现在要在“{topic}”这个类别中，选择一个具体的对象。
3: Discussion and chat。然后，另一位角色对上述介绍的内容展开对话。5段对话，每段对话不要过15个单词，可以是问题，或者陈述其他观点等等。

分几个步骤完成，以####作为分隔符
step 1: 生成短标题，包括他们要讨论的具体的对象。
step 3: 生成对话。

Example：

####
Title: <title's here>

####
Jenny:: <What are they talking about.>

Guy:: <200 words introduction or description>

Aria:: <chat>

Guy:: <chat>

Aria:: <chat>

<chat goes on, 5 exchanges total>
"""

def gen_discussion():
    
    global user_msg
    
    random.seed(time.time())
    # random.shuffle(categories)

    user_msg = user_msg.format(topic = random.choice(categories))
    
    # print(user_msg)
    
    text = gen_c2(system_msg,user_msg)
    title = [s.replace("Title:","").strip() for s in text.split("####") if "Title" in s][0]
    context = extract_lines_with_pattern(find_string_with_most_colons(text.split("####")))
    return title, context

if __name__ == "__main__":
    result = gen_discussion()
    print("\n" , result)