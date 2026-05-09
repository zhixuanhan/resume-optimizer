# -*- coding: utf-8 -*-
import re

filepath = r"C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修复 optimize_experience 函数签名
content = re.sub(
    r'def optimize_experience\(original_exp, target_job, competencies\):',
    'def optimize_experience(original_exp, target_job, competencies, supplements=None):',
    content
)

# 2. 修复 optimize_skills 函数签名
content = re.sub(
    r'def optimize_skills\(original_skills, target_job, competencies\):',
    'def optimize_skills(original_skills, target_job, competencies, supplements=None):',
    content
)

# 3. 修复调用处 - 实习经历
content = re.sub(
    r"optimized\['实习经历'\] = optimize_experience\(sections\['实习经历'\], target_job, competencies\)",
    "optimized['实习经历'] = optimize_experience(sections['实习经历'], target_job, competencies, supplements)",
    content
)

# 4. 修复调用处 - 项目经验
content = re.sub(
    r"optimized\['项目经验'\] = optimize_experience\(sections\['项目经验'\], target_job, competencies\)",
    "optimized['项目经验'] = optimize_experience(sections['项目经验'], target_job, competencies, supplements)",
    content
)

# 5. 修复调用处 - 技能证书
content = re.sub(
    r"optimized\['技能证书'\] = optimize_skills\(sections\['技能证书'\], target_job, competencies\)",
    "optimized['技能证书'] = optimize_skills(sections['技能证书'], target_job, competencies, supplements)",
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("All arguments fixed!")
print("已修复：")
print("  1. optimize_experience function signature")
print("  2. optimize_skills function signature")
print("  3. Three call sites updated with supplements parameter")
