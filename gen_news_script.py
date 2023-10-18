"""generate news  script"""
import time
import re
import os
import random
import openai
from utils import *
import ast

import bbc_reuters_news as news_source

def remove_inner_content(text):
    # 使用正则表达式找到所有的[[内容]]，并将其中的内容替换为空
    return re.sub(r'\[(.*?)\]', '[]', text)

def gen_news(url,show = True):
    """从bbc或者reuters的网页链接，获取新闻，并生成书面和口语版本的总结。

    Args:
        url: bbc或者reuters的新闻网页链接

    Returns:
        一个字典:{title, written, spoken}

    >>> result = gen_news('https://www.reuters.com/technology/biden-cut-china-off-more-nvidia-chips-expand-curbs-more-countries-2023-10-17/',show=False) # 
    >>> result['title'][0]
    'B'
    >>> len(result['written']) > 1
    True
    """
    system_msg = "Your specialty is English news writing and teaching. Please avoid any politeness, don't try to communicate with me, and just output the answers I need."

    # url = 'https://www.bbc.com/news/world-asia-china-67121520'

    news = news_source.get(url)

    cefr_level = 'B1'
    
    summarize_prompt = f"""
    - summarize the following news:
    step 1. summarize the news to 250 words in formal English, CEFR {cefr_level} level.
    step 2. summarize the news to 250 words in spoken English, CEFR {cefr_level} level but easy reading, casual chat style, short sentences.

    - Print the summary, eg:
    ```
    [step 1, Formal English Summary, 250 words, CEFR {cefr_level} Level]
    formal summary here.
    
    [step 2, Spoken English Summary, 250 words, CEFR {cefr_level} Level, Easy Reading, casual chat style, short sentences]
    spoken summary here.
    ```
    - The news to summerize:
    {news}
    """.strip()

    summary = gen_g35(system_msg, summarize_prompt, show=show)

    result = remove_inner_content(summary).strip().split("[]")

    result = [s.strip() for s in result if s.strip() != '']

    result = {'title': news['title'],
              'written': result[0],
              'spoken': result[1]}

    return result


if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    
    #print('测试完成')
    url = 'https://www.reuters.com/markets/asia/imf-says-china-property-slowdown-will-weigh-asias-growth-2023-10-18/'
    result = gen_news(url,show=True)
    #print("\n\n")
    #print(result)
