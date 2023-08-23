"""generate discuss script"""
import re
import os
import random
import openai
from utils import *
import ast


system_msg = "请你成为我的英语老师，帮我进行英语对话的练习，以及对话练习脚本的设计。"


