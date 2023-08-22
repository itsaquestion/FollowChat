import pytest
from utils import replace_placeholders  # 这里需要将your_module替换为你定义replace_placeholders函数的模块名称

def test_replace_placeholders(tmpdir):
    # 创建一个临时文件并写入一些包含占位符的文本
    file_path = tmpdir.join("test.txt")
    file_path.write("Hello {name}!")

    # 定义一个替换字典
    replacements = {
        'name': 'World',
    }

    # 使用replace_placeholders函数
    replaced_text = replace_placeholders(file_path, replacements)

    # 检查replace_placeholders的输出是否如预期
    assert replaced_text == "Hello World!"
    
def test_replace_prompt():
   replacements = {
       'context': 'At home'
   } 
   
   replaced_text = replace_placeholders('prompts/choose_relation.txt', replacements)
   
   print(replaced_text)