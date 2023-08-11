import random
import os
from datetime import datetime
from gen_script import gen_script,system_msg,user_msg
from script2wav import script2wav
from combine_wav import combine_wav,merge_mp3_files_in_directory

def pick_a_theme():
    """随机生成一个“地点-主题-对话类型”的元组，形成一句话的字符串
    """
    import random

    # 场地和主题列表
    locations = [
        {"location": "咖啡店", "topics": ["天气", "咖啡品种", "书籍或阅读", "音乐", "旅行"]},
        {"location": "办公室", "topics": ["工作任务", "会议", "团队合作", "工作压力", "职业发展"]},
        {"location": "学校", "topics": ["学习科目", "考试", "课外活动", "学习方法", "老师和同学"]},
        {"location": "超市或商店", "topics": ["食品", "价格", "促销活动", "新品上市", "健康饮食"]},
        {"location": "公园", "topics": ["运动", "季节", "动植物", "休闲活动", "环保"]},
        {"location": "家里", "topics": ["家庭成员", "日常任务", "假日计划", "家庭传统", "烹饪"]},
        {"location": "餐馆", "topics": ["菜品", "文化差异", "饮食习惯", "推荐", "餐饮经验"]},
        {"location": "医院", "topics": ["健康状况", "医生建议", "医疗保健", "预防措施", "康复"]},
        {"location": "健身房", "topics": ["锻炼方法", "健身目标", "健康生活方式", "体育运动", "健身器械"]},
        {"location": "图书馆", "topics": ["文献检索", "最近读的书", "写作", "研究项目", "学习资源"]}
    ]

    # 对话类型列表
    conversation_types = [
        "分享经验或叙述", "询问与提供信息", "表达观点或意见", "建议与推荐", 
        "辩论或争论", "谈判与协商", "安慰与鼓励", "表达感情与情感", 
        "计划与安排", "解释与阐述", "评论与评价", "指导与教学", 
        "请求与命令", "致谢与道歉"
    ]

    # 随机选择场地和主题
    selected_location = random.choice(locations)
    selected_topic = random.choice(selected_location["topics"])

    # 随机选择对话类型
    selected_type = random.choice(conversation_types)

    result = f"地点：{selected_location['location']}；主题：{selected_topic}；对话类型：{selected_type}"
    return(result)


def gen_chat_mp3():
    print("选择对话主题")
    chat_theme = pick_a_theme()
    chat_name = "_".join([x.split("：")[1].strip() for x in chat_theme.split('；')])
    print(f'{chat_theme=}')
    print(f'{chat_name=}')

    scripts_dir = 'scripts'
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
    
    print("生成对话脚本")
    script = gen_script(chat_theme, system_msg, user_msg)
    
    today = datetime.today()
    script_name = today.strftime("%Y%m%d") + "_" + chat_name + ".txt"
    
    script_path = scripts_dir + "/" + script_name
    
    print(f"写入文件{script_path}")
    with open(script_path, 'w') as f:
        f.write(script)
        
    print('生成wav文件')
    script2wav(script_path)
   
    mp3_file = today.strftime("%Y%m%d") + "_" + chat_name+".mp3"
    print(f'合并wav文件到MP3:{mp3_file}') 
    combine_wav(mp3_file,'fragments','output') 


if __name__ == "__main__":
    for i in range(3):
        print(f'生成{i}')
        gen_chat_mp3()
    
    print('合并同一天的')
    merge_mp3_files_in_directory('output')
    
    print('完成！')