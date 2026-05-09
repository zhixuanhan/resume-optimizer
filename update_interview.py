# -*- coding: utf-8 -*-
"""修改面试话术生成函数，增加数量和结合简历程度"""

import re

app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'

with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到 generate_interview_answers 函数中的 prompt 和 call_ai 行
in_function = False
prompt_start_line = None
prompt_end_line = None
call_ai_line = None

for i, line in enumerate(lines):
    if 'def generate_interview_answers' in line:
        in_function = True
    elif in_function and 'def ' in line and 'generate_interview_answers' not in line:
        # 下一个函数开始，退出
        break
    
    if in_function:
        # 找 prompt = f" 的行
        if 'prompt = f"' in line and prompt_start_line is None:
            prompt_start_line = i
            # 检查是否是单行的 prompt（末尾有 "）
            if line.rstrip().endswith('"'):
                prompt_end_line = i
        # 如果 prompt 是多行，找到结束的 "
        elif prompt_start_line is not None and prompt_end_line is None:
            if '"' in line:
                prompt_end_line = i
        
        # 找 call_ai(prompt, max_tokens=
        if 'call_ai(prompt, max_tokens=' in line:
            call_ai_line = i

print(f"Found: prompt lines {prompt_start_line}-{prompt_end_line}, call_ai at {call_ai_line}")

if prompt_start_line is not None and call_ai_line is not None:
    # 新的 prompt 内容（使用多行字符串）
    new_prompt_lines = '''    prompt = f"""你是一个资深HR面试官。请为应聘【{target_job}】岗位的候选人准备【10个】面试问题及【高度个性化】的答案。

【核心要求】
1. 每个答案必须引用候选人的真实经历，提及具体的项目名称、公司名称、技能名称
2. 用STAR法则组织答案（情境-任务-行动-结果），让回答有说服力
3. 答案要像真人在面试时说的话，口语化、自然、有细节
4. 每条答案120-180字，信息密度高
5. 问题类型要多样：2个自我介绍类、3个经历类、2个技能类、2个职业规划类、1个压力面试类

【输出格式】
Q1: 问题
A1: 答案
Q2: 问题
A2: 答案
...
Q10: 问题
A10: 答案

【候选人简历关键内容】
教育背景：{edu[:300]}
实习/项目经历：{exp[:800]}
技能证书：{skills[:400]}{supp_context}

【重要提醒】
- 答案必须是这个候选人真实能说出口的内容
- 必须出现简历里的具体信息（公司名、项目名、技能名）
- 不要编造简历里没有的经历
- 必须输出完整的10个问答，不能少

请直接输出10个Q&A："""
'''
    
    # 新的 call_ai 行
    new_call_ai = '    result = call_ai(prompt, max_tokens=5000, temperature=0.7)\n'
    
    # 替换 prompt 和 call_ai
    # 先替换 call_ai（因为 prompt 范围会变）
    if prompt_end_line is not None:
        # 多行 prompt，替换整个范围
        new_lines = lines[:prompt_start_line] + [new_prompt_lines] + lines[prompt_end_line+1:]
    else:
        # 单行 prompt
        new_lines = lines[:prompt_start_line] + [new_prompt_lines] + lines[prompt_start_line+1:]
    
    # 找到新的 call_ai 行位置并替换
    for i, line in enumerate(new_lines):
        if 'call_ai(prompt, max_tokens=2500' in line:
            new_lines[i] = new_call_ai
            print(f"Replaced call_ai at line {i}")
            break
    
    # 写回文件
    with open(app_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("SUCCESS: Updated interview function!")
    print("- 面试问答数量: 5 -> 10")
    print("- max_tokens: 2500 -> 5000")
    print("- 强化简历结合要求")
else:
    print("ERROR: Could not find prompt or call_ai in generate_interview_answers function")
