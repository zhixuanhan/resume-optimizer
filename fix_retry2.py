import re

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 用正则找整个 try...except urlopen 块并替换
# 匹配 from "    try:" 一直到 "    except (...URLError...) as e:"
pattern = r'(    try:\r?\n(?:[ \t]*\r?\n)*        with urllib\.request\.urlopen\(req, timeout=90\) as resp:\r?\n(?:[ \t]*\r?\n)*            result = json\.loads\(resp\.read\(\)\)\r?\n(?:[ \t]*\r?\n)*            return result\[\'choices\'\]\[0\]\[\'message\'\]\[\'content\'\]\.strip\(\)\r?\n)(    except \(urllib\.error\.URLError, urllib\.error\.HTTPError, Exception\) as e:)'

replacement = '''    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                result = json.loads(resp.read())
                return result['choices'][0]['message']['content'].strip()
        except socket.timeout:
            if attempt == 0:
                continue  # 重试一次
            return '[AI生成失败: The read operation timed out]'
        except Exception as e:
            return f'[AI生成失败: {str(e)}]'

'''

match = re.search(pattern, content)
if match:
    print(f'Found at position {match.start()}-{match.end()}')
    print(f'Matched group 1 (try): {repr(match.group(1)[:100])}')
    print(f'Matched group 2 (except): {repr(match.group(2))}')
    content = re.sub(pattern, replacement, content)
    print('Retry logic added successfully!')
else:
    print('ERROR: pattern not found')
    # 打印实际内容
    idx = content.find('with urllib.request.urlopen(req, timeout=90)')
    if idx >= 0:
        print('Actual content near urlopen:')
        print(repr(content[idx-50:idx+400]))

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
    f.write(content)
