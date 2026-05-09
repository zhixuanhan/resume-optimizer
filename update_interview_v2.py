# -*- coding: utf-8 -*-
"""优化面试话术生成 - 减少数量但保持质量"""

app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到面试话术的 prompt 部分并替换
# 使用更精确的定位

import re

# 查找 interview prompt 区域
# 从 "【核心要求】" 开始，到 "请直接输出" 结束

new_prompt = '''【核心要求】
1. 每个答案必须引用候选人的真实经历，提及具体的项目名称、公司名称、技能名称
2. 用STAR法则组织答案（情境-任务-行动-结果），让回答有说服力
3. 答案要像真人在面试时说的话，口语化、自然、有细节
4. 每条答案120-160字，信息密度高
5. 问题类型：1个自我介绍、2个经历类、2个技能/优缺点类、1个职业规划

【输出格式】
Q1: 问题
A1: 答案
...

【候选人简历关键内容】
教育背景：{edu[:300]}
实习/项目经历：{exp[:800]}
技能证书：{skills[:400]}{supp_context}

【重要提醒】
- 必须引用简历中的真实信息（公司名、项目名、技能名）
- 不要编造不存在的经历
- 必须输出完整的6个问答

请直接输出6个Q&A：'''

# 找到并替换
# 查找旧的 prompt 内容
old_start = '【核心要求】'
old_end = '请直接输出10个Q&A："""'

start_idx = content.find(old_start)
end_idx = content.find(old_end)

if start_idx != -1 and end_idx != -1:
    # 替换中间内容
    new_content = content[:start_idx] + new_prompt + content[end_idx + len(old_end):]
    
    # 同时修改 max_tokens
    new_content = new_content.replace('max_tokens=5000', 'max_tokens=3500')
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("SUCCESS!")
    print("- 面试问答数量: 10 -> 6")
    print("- max_tokens: 5000 -> 3500")
    print("- 保持简历结合要求")
else:
    print(f"ERROR: Could not find prompt markers (start={start_idx}, end={end_idx})")
