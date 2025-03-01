import re
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip, AudioFileClip
import numpy as np

# 解析LRC文件
def parse_lrc(lrc_path):
    lyrics = []
    with open(lrc_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            match = re.match(r'\[(\d+):(\d+\.\d+)$$(.*)', line)
            if match:
                minutes = int(match.group(1))
                seconds = float(match.group(2))
                total_time = minutes * 60 + seconds
                text = match.group(3).strip()
                lyrics.append((total_time, text))
    return sorted(lyrics, key=lambda x: x[0])

# 生成单帧歌词图像
def generate_lyric_frame(text, frame_size=(1920, 1080), font_size=60):
    img = Image.new('RGB', frame_size, color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', font_size)
    text_width = draw.textlength(text, font=font)
    draw.text(((frame_size[0]-text_width)//2, 800), text, font=font, fill=(255, 255, 255))
    return img

# 合成视频
def create_lyric_video(lrc_path, audio_path, output_path='output.mp4', fps=24):
    lyrics = parse_lrc(lrc_path)
    frames = []
    for timestamp, text in lyrics:
        frame = generate_lyric_frame(text)
        frames.append(np.array(frame))
    
    # 计算每帧持续时间（假设每句歌词持续到下一句开始）
    durations = []
    for i in range(len(lyrics)):
        if i < len(lyrics)-1:
            duration = lyrics[i+1][0] - lyrics[i][0]
        else:
            duration = 2  # 最后一句显示2秒
        durations.append(duration)
    
    # 生成视频剪辑
    clip = ImageSequenceClip(frames, durations=durations)
    audio = AudioFileClip(audio_path)
    clip = clip.set_audio(audio)
    clip.write_videofile(output_path, fps=fps)

# 执行
create_lyric_video('song.lrc', 'song.mp3')

