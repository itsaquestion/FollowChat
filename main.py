import random
import os
from datetime import datetime
# from gen_script import gen_script,system_msg,user_msg
from script2wav import script2wav
from combine_wav import combine_wav, merge_mp3_files_in_directory

from gen_chat_script import gen_chat_script
from gen_discussion_script import gen_discussion


def gen_chat_mp3():

    scripts_dir = 'scripts'
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)

    print("生成对话脚本")
    title, script = gen_chat_script()

    today = datetime.today()

    file_name = today.strftime("%Y%m%d") + "_" + 'Chat_' +  title
    script_name = file_name + ".txt"

    script_path = scripts_dir + "/" + script_name

    print(f"写入文件{script_path}")
    with open(script_path, 'w') as f:
        f.write(script)

    print('生成wav文件')
    script2wav(script_path)

    mp3_file = file_name + ".mp3"
    print(f'合并wav文件到MP3:{mp3_file}')
    combine_wav(mp3_file, 'fragments', 'output')

def gen_discussion_mp3():
    scripts_dir = 'scripts'
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)

    print("生成讨论脚本")
    title, script = gen_discussion()

    today = datetime.today()

    file_name = today.strftime("%Y%m%d") + "_" + 'Disc_' +  title
    script_name = file_name + ".txt"

    script_path = scripts_dir + "/" + script_name

    print(f"写入文件{script_path}")
    with open(script_path, 'w') as f:
        f.write(script)

    print('生成wav文件')
    script2wav(script_path)

    mp3_file = file_name + ".mp3"
    print(f'合并wav文件到MP3:{mp3_file}')
    combine_wav(mp3_file, 'fragments', 'output')



if __name__ == "__main__":
    for i in range(1):
        print(f'生成对话{i}')
        gen_chat_mp3()

    for i in range(1):
        print(f'生成讨论{i}')
        gen_discussion_mp3()

    print('合并同一天的')
    merge_mp3_files_in_directory('output')

    print('完成！')
