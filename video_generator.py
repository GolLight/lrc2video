import os

from moviepy.video.VideoClip import ColorClip, TextClip, ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy import vfx, afx


def generate_video(title, lrc_entries, audio_file, output_file, video_size=(1280,720),
                    fps=24, bg_color=(0,0,0)):
    """
    根据 lrc 歌词条目和音频文件生成动态歌词视频。

    参数：
    - title 视频开始标题
    - lrc_entries: 列表，每个元素为 (start_time, end_time, lyric)
    - audio_file: wav 音频文件路径
    - output_file: 输出视频文件路径
    - video_size: 视频分辨率，默认 1280x720
    - fps: 帧率，默认 24
    - bg_color: 背景颜色，默认黑色
    """
    # 加载音频文件
    audio_clip = AudioFileClip(audio_file)
    duration = audio_clip.duration
    
    # 创建背景视频（纯色）
    # background = ColorClip(size=video_size, color=bg_color, duration=duration)

    # 创建背景视频（图片）
    background = ImageClip("songs/test1.jpg").with_duration(duration)
    
    # 创建歌词文本剪辑列表
    text_clips = []
    print(lrc_entries[0])
    title_duration = lrc_entries[0][0] - 1;
    if title_duration < 0:
        title_duration = 0;
    txt_clip = TextClip(text=title, font_size=200, color='orange', font='fonts/MoonStarsKaiTTC/MoonStarsKai-Regular.ttc')
    txt_clip = txt_clip.with_position('center').with_start(0).with_duration(lrc_entries[0][0])
    for start, end, lyric in lrc_entries:
        # 如果 end 为 None 或超出音频总时长，则设置为总时长
        if end is None or end > duration:
            end = duration
        duration_clip = end - start
        if duration_clip <= 0:
            continue
        # 创建文本剪辑（可根据需要调整 fontsize、color、font 等参数）
        # txt_clip = TextClip(text=lyric, font_size=50, color='blue', font='fonts/MoonStarsKaiTTC/MoonStarsKai-Regular.ttc')
        # txt_clip = txt_clip.with_position('center').with_start(start).with_duration(duration_clip)
        
        try:
            # 带阴影的文字（参考网页5特效）
            txt_clip = TextClip(text=lyric, font_size=100, color='bule', 
                              font='fonts/MoonStarsKaiTTC/MoonStarsKai-Regular.ttc', 
                              stroke_color='black', stroke_width=1)
        except:
            txt_clip = TextClip(text=lyric, font_size=100, color='blue', font='fonts/MoonStarsKaiTTC/MoonStarsKai-Regular.ttc')
            
        # 动态位置（参考网页2滚动逻辑）
        txt_clip = (txt_clip.with_position(lambda t: ('center', 720 - 80*(t-start)))
                   .with_start(start)
                   .with_duration(duration_clip)
                   .with_effects([vfx.FadeIn(3)])
                    )   
                #    .fx(vfx.fadein, 0.3))


        text_clips.append(txt_clip)
    
    # # 叠加背景和歌词文本剪辑
    # video = CompositeVideoClip([background] + text_clips)
    # video = video.with_audio(audio_clip)
    
    # # 输出视频文件
    # video.write_videofile(output_file, fps=fps)

      # 合成视频（带内存优化）
    video = CompositeVideoClip([background] + text_clips, 
                              use_bgclip=True).with_audio(audio_clip)
    video.write_videofile(output_file, fps=fps, threads=4, 
                        preset='fast', audio_codec='aac')

if __name__ == '__main__':
    # 示例调用（仅用于测试）
    sample_entries = [(0, 5, "Hello World"), (5, 10, "动态歌词示例")]
    generate_video(sample_entries, 'example.wav', 'output.mp4')
