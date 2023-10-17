"""generate news  script"""
import time
import re
import os
import random
import openai
from utils import *
import ast

import bbc_reuters_news as news_source


def gen_news(url,show = True):
    """从bbc或者reuters的网页链接，获取新闻，并生成书面和口语版本的总结。

    Args:
        url: bbc或者reuters的新闻网页链接

    Returns:
        一个字典:{title, written, spoken}

    >>> result = gen_news('https://www.bbc.com/news/world-asia-china-67121520',show=False) # 
    >>> result['title'][0]
    'P'
    >>> len(result['written']) > 1
    True
    """
    system_msg = "你的特长是英语写作和教学。请你避免任何客套话，不要尝试和我交流，直接输出我需要的答案。"

    # url = 'https://www.bbc.com/news/world-asia-china-67121520'

    news = news_source.get(url)

    summarize_prompt = f"""
    - Summarize the following news to 250 words.  let's do it by steps.  
    step 1: summary. summarize the news to formal written English about 250 words, CEFR B1 level. No more than 3 paragraphs.
    step 2: spoken version. rewrite your summary into spoken English, make it easy to speak. CEFR B1 level. No more than 3 paragraphs.

    - Print the summary only, use #### after step notes. eg:
    (step 1, formal English summary, about 250 words, CEFR B1 level, No more than 3 paragraphs.) ####
    (step 2, spoken version, about 250 words, CEFR B1 level, No more than 3 paragraphs.) ####

    - The news to summerize:
    {news}
    """.strip()

    summary = gen_g35(system_msg, summarize_prompt, show)

    result = re.sub(r'\([^)]*\)', '', summary).strip().split("####")

    result = [s.strip() for s in result if s.strip() != '']

    result = {'title': news['title'],
              'written': result[0],
              'spoken': result[1]}

    return result





if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print('测试完成')