# %%

from datetime import datetime
from gen_news_script import gen_news
import os
from script2wav import script2wav
from combine_wav import combine_wav, merge_mp3_files_in_directory
from utils import sanitize_filename
# %%


def gen_voice_from_news(url):
    scripts_dir = 'scripts'
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)

    print('生成新闻总结')
    # 'https://www.bbc.com/news/technology-67133155'
    result = gen_news(url, show=True)

    today = datetime.today()

    file_name = today.strftime("%Y%m%d") + "_" + 'News_' + result['title']
    file_name = sanitize_filename(file_name)
    
    script_name = file_name + ".txt"

    script_path = scripts_dir + "/" + script_name

    script = "Aria: " + result['title'] + '. ' + result['spoken']
    script = script.replace('\n', '')

    print(f"写入文件{script_path}")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)

    print('生成wav文件')
    script2wav(script_path)

    mp3_file = file_name + ".mp3"
    print(f'合并wav文件到MP3:{mp3_file}')
    combine_wav(mp3_file, 'fragments', 'output')



if __name__ == "__main__":
    # urls = [#'https://www.bbc.com/news/technology-67132846',
    #         #'https://www.bbc.com/news/business-67121459',
    #         'https://www.bbc.com/news/business-67118263',
    #         'https://www.bbc.com/news/science-environment-67101176',
    #         ]
    
    # for url in urls:
    #     gen_voice_from_news(url)
        
    print('合并同一天的')
    merge_mp3_files_in_directory('output')

    print('完成！')