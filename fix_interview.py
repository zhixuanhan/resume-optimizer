# -*- coding: utf-8 -*-
"""
修复三个问题:
1. 职业规划板块：让用户自由输入文本（不按关键词分），AI根据用户输入+缺失关键词一起优化
2. 简历优化输出：经历描述前加小标题
3. 面试Q&A：结合用户自身经历生成个性化回答
"""

import re

def fix_app_py():
    with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 修改 optimize_experience 函数 - 添加小标题
    old_optimize_exp = '''def optimize_experience(original_exp, target_job, competencies, supplements=None):
    """用 AI 优化实习/项目经历描述"""
    comp_str = '、'.join(competencies[:5]) if competencies else '运营、策划、数据分析'
    prompt = f"你是一个资深HR。请将以下实习/项目经历用STAR法则优化重写，使其更专业、更有针对性。要求：1)STAR结构(情境-任务-行动-结果)2)动词开头：负责、主导、推进、优化、搭建、分析等 3)量化成果，加具体数字 4)融入关键词：{comp_str} 5)每条2-4行 6)直接输出不加说明\\n原始内容：{original_exp}\\n优化后："
    result = call_ai(prompt, max_tokens=1200, temperature=0.7)
    return result'''
    
    new_optimize_exp = '''def optimize_experience(original_exp, target_job, competencies, supplements=None):
    """用 AI 优化实习/项目经历描述"""
    comp_str = '、'.join(competencies[:5]) if competencies else '运营、策划、数据分析'
    
    # 将用户的补充内容加入 prompt
    supp_context = ''
    if supplements:
        supp_lines = []
        for kw, detail in supplements.items():
            if detail and detail.strip():
                supp_lines.append(f'用户补充的经历（{kw}）：{detail.strip()}')
        if supp_lines:
            supp_context = '\\n用户补充的相关经历：\\n' + '\\n'.join(supp_lines)
    
    prompt = f"你是一个资深HR。请将以下实习/项目经历用STAR法则优化重写，使其更专业、更有针对性。要求：1)每段经历先写小标题（格式：公司名/项目名，岗位/角色，核心能力）：然后换行写具体内容 2)STAR结构(情境-任务-行动-结果) 3)动词开头：负责、主导、推进、优化、搭建、分析等 4)量化成果，加具体数字 5)融入关键词：{comp_str} 6)每条2-4行 7)直接输出不加说明\\n原始内容：{original_exp}{supp_context}\\n优化后："
    result = call_ai(prompt, max_tokens=1500, temperature=0.7)
    return result'''
    
    if old_optimize_exp in content:
        content = content.replace(old_optimize_exp, new_optimize_exp)
        print("1. optimize_experience 已更新（添加小标题+用户补充内容）")
    else:
        print("1. optimize_experience 未找到匹配，尝试regex...")
        # 尝试正则匹配
        pattern = r'def optimize_experience\(original_exp, target_job, competencies, supplements=None\):[\s\S]*?return result'
        match = re.search(pattern, content)
        if match:
            content = content[:match.start()] + new_optimize_exp + content[match.end():]
            print("1. optimize_experience 已通过regex更新")
    
    # 2. 修改 generate_interview_answers 函数 - 结合用户经历
    old_interview = '''def generate_interview_answers(sections, target_job, career_key):
    """用 AI 生成个性化面试答案"""
    exp = sections.get('实习经历', '') or sections.get('项目经验', '') or sections.get('校园经历', '')
    skills = sections.get('技能证书', '')
    
    prompt = f"你是一个资深HR面试官。请为应聘【{target_job}】岗位的候选人准备5个最常见的面试问题及个性化答案。\\n要求：\\n1) 答案要结合候选人实际经历，不要空洞套话\\n2) 用STAR法则回答经历类问题\\n3) 每条答案100字左右\\n4) 直接输出，格式：Q1: 问题\\nA1: 答案\\n\\n候选人简历关键内容：\\n经历：{exp[:500]}\\n技能：{skills[:300]}\\n\\n直接输出5个Q&A："
    
    result = call_ai(prompt, max_tokens=2000, temperature=0.7)
    return result'''
    
    new_interview = '''def generate_interview_answers(sections, target_job, career_key, supplements=None):
    """用 AI 生成个性化面试答案 - 结合用户实际经历"""
    exp = sections.get('实习经历', '') or sections.get('项目经验', '') or sections.get('校园经历', '') or sections.get('其他', '')
    skills = sections.get('技能证书', '')
    edu = sections.get('教育经历', '')
    
    # 将用户的补充内容加入
    supp_context = ''
    if supplements:
        supp_lines = []
        for kw, detail in supplements.items():
            if detail and detail.strip():
                supp_lines.append(f'用户补充的「{kw}」相关经历：{detail.strip()}')
        if supp_lines:
            supp_context = '\\n用户补充的额外经历：\\n' + '\\n'.join(supp_lines)
    
    prompt = f"你是一个资深HR面试官。请为应聘【{target_job}】岗位的候选人准备5个最常见的面试问题及【高度个性化】的答案。\\n要求：\\n1) 答案必须紧密结合候选人的实际经历，用具体事例说明\\n2) 用STAR法则回答经历类问题（情境-任务-行动-结果）\\n3) 答案中要出现候选人真实做过的项目、实习、技能名称\\n4) 每条答案150字左右，信息密度高\\n5) 直接输出，格式：Q1: 问题\\nA1: 答案\\n\\n候选人简历关键内容：\\n教育背景：{edu[:200]}\\n实习/项目经历：{exp[:600]}\\n技能：{skills[:300]}{supp_context}\\n\\n注意：答案必须是这个候选人能说出口的真实内容，不要编造不存在的东西！\\n直接输出5个Q&A："
    
    result = call_ai(prompt, max_tokens=2500, temperature=0.7)
    return result'''
    
    if old_interview in content:
        content = content.replace(old_interview, new_interview)
        print("2. generate_interview_answers 已更新（结合用户真实经历）")
    else:
        print("2. generate_interview_answers 未找到匹配，尝试regex...")
        pattern = r'def generate_interview_answers\(sections, target_job, career_key\):[\s\S]*?return result'
        match = re.search(pattern, content)
        if match:
            content = content[:match.start()] + new_interview + content[match.end():]
            print("2. generate_interview_answers 已通过regex更新")
    
    # 3. 找到调用 generate_interview_answers 的地方，传入 supplements 参数
    # 在 /api/optimize 路由中
    old_call = 'interview_ai = generate_interview_answers(sections, target_job, career_key)'
    new_call = 'interview_ai = generate_interview_answers(sections, target_job, career_key, supplements)'
    
    if old_call in content:
        content = content.replace(old_call, new_call)
        print("3. generate_interview_answers 调用处已添加 supplements 参数")
    else:
        print("3. 未找到 generate_interview_answers 调用，可能已修改过")
    
    with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\\n=== 修复完成 ===")

if __name__ == '__main__':
    fix_app_py()
