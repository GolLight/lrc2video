from lrc_parser import parse_lrc

from moviepy.editor import AudioFileClip, CompositeVideoClip, ColorClip, TextClip
from moviepy.video.fx.all import fadein, fadeout

def create_lyric_clips(lyrics, duration, font='Arial', fontsize=50, color='white'):
    clips = []
    for i in range(len(lyrics)):
        start_time, text = lyrics[i]
        end_time = lyrics[i+1][0] if i < len(lyrics)-1 else duration
        
        # 创建单句歌词的文本片段
        txt_clip = TextClip(text, fontsize=fontsize, font=font, color=color)
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_start(start_time).set_end(end_time)
        txt_clip = txt_clip.fx(fadein, 0.5).fx(fadeout, 0.5)  # 添加渐入渐出效果
        clips.append(txt_clip)
    return clips

def generate_video(audio_path, lrc_path, output_path, bg_color=(0,0,0)):
    # 解析歌词和音频
    lyrics = parse_lrc(lrc_path)
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    
    # 创建背景和歌词片段
    background = ColorClip(size=(1280, 720), color=bg_color, duration=duration)
    lyric_clips = create_lyric_clips(lyrics, duration)
    
    # 合成视频
    final_clip = CompositeVideoClip([background] + lyric_clips).set_audio(audio_clip)
    final_clip.write_videofile(output_path, fps=24, codec='libx264')

generate_video(
    audio_path="song.mp3",
    lrc_path="song.lrc",
    output_path="output_video.mp4",
    bg_color=(0, 0, 0)  # 黑色背景
)
