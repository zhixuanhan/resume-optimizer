# -*- coding: utf-8 -*-
import re

filepath = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 修改调用处
old = 'interview_ai = generate_interview_answers(sections, target_job, matched_key)'
new = 'interview_ai = generate_interview_answers(sections, target_job, matched_key, supplements)'

if old in content:
    content = content.replace(old, new)
    print("已修改 generate_interview_answers 调用，添加 supplements 参数")
else:
    print("未找到旧调用，可能已修改")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("完成")
