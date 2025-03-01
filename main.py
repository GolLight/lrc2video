import sys
from lrc_parser import parse_lrc
from video_generator import generate_video

# python main.py "The truth that you leave-Haha Light"  "songs/lyrics/The truth that you leave-Haha Light.lrc" "songs/the truth that you leave.wav"  output/output.mp4
def main():
    if len(sys.argv) < 4:
        print("用法: python main.py title <lrc_file> <wav_file> <output_video>")
        sys.exit(1)
    title = sys.argv[1]
    lrc_file = sys.argv[2]
    wav_file = sys.argv[3]
    output_video = sys.argv[4]
    
    # 解析 lrc 文件
    lrc_entries = parse_lrc(lrc_file)
    
    # 生成视频
    generate_video(title, lrc_entries, wav_file, output_video)
    
if __name__ == '__main__':
    main()
