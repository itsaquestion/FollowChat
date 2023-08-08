"""用于把字符转化语音文件
"""
import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

def tts2file(text, speaker, file_path, style = 'excited', style_degree='0.3', debug = False):
    """字符转为语音文件

    Args:
        text (str): 要说的字符，如'Hello!'
        speaker (str): 角色，如'Jenny'
        file_path (str): 保存文件的路径，如'output/001.wav'
        style (str, optional): 说话风格. Defaults to 'excited'.
        style_degree (str, optional): 风格的强度. Defaults to '0.3'.
        debug (bool, optional): 是否显示SSML字符串. Defaults to False.
    """
    with open('ssml_template.xml', 'r') as f:
        template = f.read()
    ssml_string = template.format(speaker = speaker, text = text,style=style,style_degree=style_degree)
    
    if debug:
        print(ssml_string)
    result = speech_synthesizer.speak_ssml_async(ssml_string).get()


    stream = speechsdk.AudioDataStream(result)
    stream.save_to_wav_file(file_path)


if __name__ == "__main__":
    text = 'Aria, have you ever considered visiting London? The history and architecture there are truly fascinating.'

    tts2file(text,'Jenny','output/001.wav',debug=True)

    text = "Oh, Jenny, I've always wanted to! I've heard so much about the British Museum and the Tower of London. Are they as impressive as people say?"

    tts2file(text,'Aria','output/002.wav')
