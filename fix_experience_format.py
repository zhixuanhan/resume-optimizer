# -*- coding: utf-8 -*-
"""精准修复经历输出格式问题"""
import re

app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# 修复1: 在 optimize_experience 函数中：
# - 增加 max_tokens 1500->2000
# - 添加输出清理逻辑
old_pattern = (
    'call_ai(prompt, max_tokens=1500, temperature=0.7)\n\n\n\n'
    '    return result\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
)

new_code = '''call_ai(prompt, max_tokens=2000, temperature=0.7)
    result_text = result
    # 清理多余的section标题和重复空行
    lines = result_text.split('\\n')
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if not prev_empty:
                cleaned_lines.append('')
                prev_empty = True
            continue
        prev_empty = False
        # 跳过多余的section标记（如【实习经历】【项目经验】【公司名/项目名】）
        if re.match(r'^【.+】$', stripped):
            continue
        # 移除行内多余空格，但保留结构
        line_clean = ' '.join(stripped.split())
        cleaned_lines.append(line_clean)
    # 移除开头和结尾的空行
    while cleaned_lines and not cleaned_lines[0]:
        cleaned_lines.pop(0)
    while cleaned_lines and not cleaned_lines[-1]:
        cleaned_lines.pop()
    return '\\n'.join(cleaned_lines)
'''

if old_pattern in content:
    content = content.replace(old_pattern, new_code)
    changes.append("OK: optimize_experience max_tokens 1500->2000 + 添加清理逻辑")
else:
    changes.append("FAIL: 未找到 optimize_experience 的原始 return 模式")
    # 尝试其他方式
    idx = content.find('call_ai(prompt, max_tokens=1500, temperature=0.7)')
    if idx >= 0:
        # 检查这是否在 optimize_experience 中
        before = content[max(0,idx-500):idx]
        if 'def optimize_experience' in before:
            # 找到了，尝试直接替换
            end = content.find('return result', idx)
            if end >= 0:
                end += len('return result')
                print(f"Found at idx={idx}, end={end}")
                print("Context:")
                print(repr(content[idx:end]))

# 修复2: 检查 SyntaxError - 查找是否有未闭合的三引号字符串
# 具体检查 line 5841 附近
line_5841_area = content
lines_list = content.split('\n')
if len(lines_list) >= 5841:
    around_error = '\n'.join(lines_list[5830:5850])
    changes.append(f"\nLine 5835-5850 area:\n{around_error}")

# 检查三引号配对
import re
triple_quote_positions = [m.start() for m in re.finditer(r'"""', content)]
if len(triple_quote_positions) % 2 != 0:
    changes.append(f"WARN: 三引号数量为奇数 ({len(triple_quote_positions)}个)")
else:
    changes.append(f"OK: 三引号配对正常 ({len(triple_quote_positions)}个)")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

for c in changes:
    print(c)
