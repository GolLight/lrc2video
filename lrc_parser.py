import re
from typing import List, Tuple

def parse_lrc(file_path: str) -> List[Tuple[float, str]]:
    lyrics = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 支持 [mm:ss.xx] 和 [mm:ss.xxx] 格式[1,4](@ref)
            match = re.match(r'$$(\d+):(\d+\.\d+)$$(.*)', line.strip())
            if match:
                minutes = int(match.group(1))
                seconds = float(match.group(2))
                timestamp = minutes * 60 + seconds
                text = match.group(3).strip()
                lyrics.append((timestamp, text))
    return sorted(lyrics, key=lambda x: x[0])