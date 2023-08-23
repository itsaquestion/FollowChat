"""
把对话文本，首先进行按完整的句子进行断句，然后转为语音，按顺序保存为001.wav等文件
"""
import re
from tts2file import tts2file
import shutil
import os

def split_sentence(text):
    """Split the given text into sentences."""
    # Using regex to split sentences by ., !, and ?
    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences

def process_chat(chat_content):
    processed_lines = []
    lines = chat_content.split("\n")
    
    buffer_sentence = ""  # Buffer to hold short sentences
    for line in lines:
        if line.strip() == "":
            continue
        
        name, sentence = line.split(": ", 1)
        sentences = split_sentence(sentence)
        
        for sent in sentences:
            # Check for short sentences
            if len(sent.split()) <= 2 and buffer_sentence == "":
                buffer_sentence = sent
                continue
            
            # If there is a sentence in buffer
            if buffer_sentence:
                processed_lines.append(f"{name}: {buffer_sentence} {sent}")
                buffer_sentence = ""
            else:
                processed_lines.append(f"{name}: {sent}")
    
    return "\n".join(processed_lines)


def script2wav(script_file,output_dir='fragments'):
    """把原始对话文本，首先重新断句，然后转化音频文件，按顺序命名为001.wav,002.wav

    Args:
        script_file (str): 对话脚本文件，如'chat.txt'
        output_dir (_type_): 输出wav文件的目录
    """
    with open(script_file, "r") as file:
        chat_content = file.read()
    
    processed_chat_content = process_chat(chat_content)

    # 如果output文件夹存在，则删除
    if os.path.exists(output_dir):
        print(f'{output_dir}目录存在，删除')
        shutil.rmtree(output_dir)

    # 创建新的output文件夹
    os.mkdir(output_dir)

    counter = 0
    for chat in processed_chat_content.split('\n'):
        counter += 1
        print(counter)
        if not '::' in chat:
            continue
        speaker, text = [x.strip() for x in chat.split('::')]
        tts2file(text,speaker,output_dir + '/'+'{:0>3}'.format(counter) + '.wav')

# %%

if __name__ == "__main__":
    script2wav('chat_sample.txt')