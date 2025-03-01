# import re
# from typing import List, Tuple

# def parse_lrc(file_path: str) -> List[Tuple[float, str]]:
#     lyrics = []
#     with open(file_path, 'r', encoding='utf-8') as f:
#         for line in f:
#             # 支持 [mm:ss.xx] 和 [mm:ss.xxx] 格式[1,4](@ref)
#             match = re.match(r'$$(\d+):(\d+\.\d+)$$(.*)', line.strip())
#             if match:
#                 minutes = int(match.group(1))
#                 seconds = float(match.group(2))
#                 timestamp = minutes * 60 + seconds
#                 text = match.group(3).strip()
#                 lyrics.append((timestamp, text))
#     return sorted(lyrics, key=lambda x: x[0])


#### 3. lrc_parser.py

# 用于解析 lrc 文件，提取每行歌词的开始时间、结束时间（由下一行开始时间确定）及歌词文本。

import re

def parse_lrc(lrc_path):
    """
    解析 lrc 歌词文件，返回一个列表，每个元素为元组 (start_time, end_time, lyric)。
    如果是最后一行歌词，end_time 为 None，后续在视频生成时处理为音频总时长。
    """
    pattern = re.compile(r'\[(\d+):(\d+\.?\d*)\](.*)')
    entries = []
    with open(lrc_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 允许一行中存在多个时间戳
            matches = pattern.findall(line)
            if matches:
                for match in matches:
                    minutes = int(match[0])
                    seconds = float(match[1])
                    start_time = minutes * 60 + seconds
                    lyric = match[2].strip()
                    if lyric:  # 只添加非空歌词
                        entries.append((start_time, lyric))
    # 按时间排序
    entries.sort(key=lambda x: x[0])
    # 为每个条目添加结束时间，结束时间为下一条目的开始时间
    entries_with_end = []
    for i, (start, lyric) in enumerate(entries):
        if i < len(entries) - 1:
            end_time = entries[i+1][0]
        else:
            end_time = None  # 最后一行，后续使用音频总时长填充
        entries_with_end.append((start, end_time, lyric))
    return entries_with_end

if __name__ == '__main__':
    # 测试用例
    lrc_path = 'example.lrc'
    entries = parse_lrc(lrc_path)
    for entry in entries:
        print(entry)
