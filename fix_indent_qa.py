# -*- coding: utf-8 -*-
import re

file_path = r"C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复 qa_list 行的缩进问题
# 查找 "qa_list = session_data.get('interview_ai')" 这一行
# 它应该在 if career_key 块内部，需要缩进

# 方法：找到这行并在前面加上8个空格（两层缩进）
old_line = "qa_list = session_data.get('interview_ai') or CAREER_DB[career_key].get('interview_qa', [])"
new_line = "        qa_list = session_data.get('interview_ai') or CAREER_DB[career_key].get('interview_qa', [])"

# 替换
content = content.replace(old_line, new_line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed!")
