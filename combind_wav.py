import os

audio_files = sorted([f for f in os.listdir('output') if f.endswith('.wav')])
audio_files

from pydub import AudioSegment

# 初始化一个空的音频段
combined_audio = AudioSegment.empty()

# 遍历每个音频文件
for audio_file in audio_files:
    # 加载音频
    audio = AudioSegment.from_wav(os.path.join('output', audio_file))
    
    # 创建一个等长的静音段
    silence = AudioSegment.silent(duration=len(audio))
    
    # 合并音频和静音段
    segment_to_add = audio + silence + audio + silence
    
    # 添加到总的音频段
    combined_audio += segment_to_add

# 保存合并后的音频
output_path = os.path.join('output', "combined_audio.wav")
combined_audio.export(output_path, format="wav")

output_path
