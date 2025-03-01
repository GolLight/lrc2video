# 动态歌词视频生成项目

该项目通过 Python 代码，将一个 lrc 歌词文件和一个 wav 音频文件合成为一个动态歌词视频。

## 项目结构

DynamicLyricsProject/ ├── main.py ├── lrc_parser.py ├── video_generator.py ├── requirements.txt └── README.md

## 安装依赖

确保你已安装 Python 3.x，然后运行下面命令安装依赖：

```bash
pip install -r requirements.txt
使用方法
在命令行中运行：

bash
复制
编辑
python main.py <lrc_file> <wav_file> <output_video>
例如：

bash
复制
编辑
python main.py "The truth that you leave-Haha Light"  "songs/lyrics/The truth that you leave-Haha Light.lrc" "songs/the truth that you leave.wav"  output/output.mp4
文件说明
main.py：项目入口，解析命令行参数并调用歌词解析和视频生成模块。
lrc_parser.py：解析 lrc 歌词文件，提取时间戳和歌词内容。
video_generator.py：利用 moviepy 库生成带有动态歌词的视频。
requirements.txt：项目依赖列表。
README.md：项目说明文件。
注意事项
lrc 文件格式应类似如下格式，每行包括时间戳与歌词内容：

[00:16.920]我喜欢那个夏天，我躲在你的怀里面
[00:24.480]我记得你的笑脸，干净得容不下沉淀
视频生成时会使用黑色背景，并在合适的时间显示歌词文本，你可以根据需要修改字体、字号、颜色等参数。