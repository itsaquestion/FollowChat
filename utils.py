"""
这个模块提供了一些实用的工具函数，包括替换字符串中的占位符。

函数列表：
- replace_placeholders：读取文件内容，并将文件中的占位符替换为指定的文本。
"""
import re
import random


def replace_placeholders(file_path, replacements):
    """
    读取文件内容，并将文件中的占位符替换为指定的文本。

    Args:
        file_path (str): 需要替换占位符的文件的路径。
        replacements (dict): 一个字典，其中的键值对表示占位符和对应的替换文本。

    Returns:
        str: 替换占位符后的文件内容。
    """
    # 打开并读取文件
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()

    # 替换所有占位符
    for placeholder, replacement in replacements.items():
        file_contents = file_contents.replace(
            "{" + placeholder + "}", f'{replacement}')

    return file_contents


def weighted_random_choose(dictionary):
    # 将概率值单位化
    total_weight = sum(dictionary.values())
    normalized_weights = {key: value /
                          total_weight for key, value in dictionary.items()}

    # 使用随机数选择一个键
    random_value = random.random()
    cumulative_weight = 0

    for key, weight in normalized_weights.items():
        cumulative_weight += weight
        if random_value <= cumulative_weight:
            return key

    # 如果无法选择键，则返回 None 或引发异常，具体根据需求决定
    return None


def extract_bracket_contents(string):
    pattern = r'\{[^{}]+\}'
    matches = re.findall(pattern, string)
    return matches[0]


def find_string_with_most_colons(strings):
    max_colon_count = 0
    max_colon_string = ""

    for string in strings:
        colon_count = string.count("::")
        if colon_count > max_colon_count:
            max_colon_count = colon_count
            max_colon_string = string

    return max_colon_string.strip()


def extract_lines_with_pattern(text, pattern=r"::"):
    lines = text.split("\n")
    matches = [line for line in lines if re.search(pattern, line)]
    return '\n\n'.join(matches).strip()
