import os
from moviepy.video.VideoClip import ColorClip, TextClip, ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io import ImageSequenceClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy import vfx
import numpy as np

def generate_video(title, lrc_entries, audio_file, output_file, video_size=(1280,720),
                   fps=24, bg_color=(0,0,0)):
    """
    根据 lrc 歌词条目和音频文件生成动态歌词视频
    
    参数优化：
    - 增加标题安全处理：当无歌词时显示完整标题
    - 优化歌词滚动动画参数
    - 修复颜色参数拼写错误
    """
    # 加载音频文件
    audio_clip = AudioFileClip(audio_file)
    duration = audio_clip.duration
    
    # 创建背景（优先使用图片，不存在时使用纯色背景）
    # image_dir = "songs/image"
    # image_files = sorted([os.path.join(image_dir, f) for f in os.listdir(image_dir)])
    # print(image_files)
    # per_image_duration = 2  #TODO 每张图片显示2秒
    if os.path.exists("songs/image/test1.jpg"):
        background = ImageClip("songs/image/test1.jpg").with_duration(duration).resized(video_size)
        # background = ImageSequenceClip(sequence=image_files, durations=[per_image_duration]*len(image_files))
        # background = background.loop(duration=duration)
    else:
        background = ColorClip(size=video_size, color=bg_color, duration=duration)

    # 标题处理逻辑优化
    text_clips = []
    if title:
        title_duration = 3  # 固定标题显示3秒
        if lrc_entries:
            title_duration = min(lrc_entries[0][0], 10)  # 取歌词出现时间和3秒的最小值
            
        txt_clip = TextClip(
            text=title, 
            font_size=70, 
            color='orange',
            font='fonts/MoonStarsKaiTTC/MoonStarsKai-Regular.ttc',
            stroke_color='black', 
            stroke_width=1
        ).with_position('center').with_duration(title_duration)
        text_clips.append(txt_clip)

    line_height = 80  # 行间距
    base_y = video_size[1] * 0.3  # 首句中间位置

    # 歌词处理优化
    for idx, (start, end, lyric) in enumerate(lrc_entries):
        end = min(end if end else duration, duration)  # 处理结束时间
        
        duration_clip = end - start
        
        if duration_clip <= 0:
            continue

        if start >= duration:
            continue

        # 创建带特效的歌词文本
        txt_clip = TextClip(
            text=lyric,
            font_size=60,
            color='blue',  # 修正颜色拼写
            font='fonts/MoonStarsKaiTTC/MoonStarsKai-Regular.ttc',
            stroke_color='white',
            stroke_width=1
        )
        
        # 优化动画参数：从底部到中部滚动
        scroll_height = video_size[1] / 2  # 滚动到屏幕中部
        scroll_speed = scroll_height / duration_clip  # 根据持续时间计算速度
        
        total_duration = duration_clip  # 歌词总时长
        fall_duration = 1.5        # 下落动画持续时间（前X秒下落）
        move_down_duration = 2.0  # 下移出屏幕的时间
        stay_duration = max(total_duration - fall_duration - move_down_duration, 1)
        start_y = -txt_clip.h      # 初始Y位置（完全在屏幕上方外）
        end_y = (video_size[1] - txt_clip.h) / 2  # 最终Y位置（垂直居中）
# 动态位置函数
        def position_func(t):
            global_y = base_y + (idx%3) * line_height  # 根据行号计算基准位置
            if t < fall_duration:
            #  # 下落阶段：二次缓动函数 (0->1)
            #     progress = min(t / fall_duration, 1.0)
            #     ease_progress = progress ** 0.5  # 缓出效果
            #     current_y = start_y + (end_y - start_y) * ease_progress
                progress = t / fall_duration
                y = np.interp(progress, [0, 1], [-txt_clip.h, global_y])
                # 阶段2：停留 (1.5~3.5s)
            elif t < fall_duration + stay_duration:
                y = global_y
            else:
                # # 阶段3：下移出屏幕 (3.5~5.5s) 
                progress = (t - fall_duration - stay_duration) / move_down_duration
                y = global_y + progress * (video_size[1] - global_y)
            return ('center', y)
        txt_clip = (txt_clip
                   .with_start(start - 1) # 提前1秒出现
                   .with_duration(duration_clip + 1) # 总时长+1秒衔接
                   .with_effects([vfx.FadeIn(1), vfx.FadeOut(1)]) 
                   .with_position(position_func)
                ) 
        
        print(lyric)
        text_clips.append(txt_clip)

    # 合成视频（带内存优化）
    video = CompositeVideoClip([background] + text_clips, 
                               use_bgclip=True).with_audio(audio_clip)
    
    # 优化输出参数
    video.write_videofile(
        output_file, 
        fps=fps,
        threads=4,
        preset='fast',
        audio_codec='aac',
        ffmpeg_params=['-movflags', '+faststart']  # 支持流式播放
    )


if __name__ == '__main__':
    # 修正后的示例调用
    sample_entries = [
        (1, 4, "♪ 前奏音乐 ♪"),
        (4, 8, "你好世界"),
        (8, 12, "动态歌词示例"),
        (12, 16, "电影py创作")
    ]
    generate_video(
        title="示例歌曲",  # 添加标题参数
        lrc_entries=sample_entries,
        audio_file='example.wav',
        output_file='output.mp4'
    )