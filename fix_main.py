# -*- coding: utf-8 -*-
"""
Fix strategy for resume-optimizer:
1. Make AI call timeouts shorter (20s) so partial results always return
2. Add try-except in generate_optimized_resume to show content even if sub-calls fail
3. Return {"error": "...", ...partial data...} when failures happen
4. The call_ai function already returns "[AI生成失败: ...]" on timeout - those become content
"""

import re

content = open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8').read()
original = content

# === FIX 1: call_ai timeout 60s → 20s ===
# 20s is enough for most calls; on timeout returns "[AI生成失败: ...]" which becomes content
old = 'with urllib.request.urlopen(req, timeout=60) as resp:'
new = 'with urllib.request.urlopen(req, timeout=20) as resp:'
count = content.count(old)
print('F1: call_ai timeout 60s→20s:', count, 'replacements')
content = content.replace(old, new, 1)

# === FIX 2: generate_optimized_resume - wrap each AI call in try-except ===
# Find generate_optimized_resume function
idx = content.find('def generate_optimized_resume(')
end = content.find('\n@app.route', idx)  # next route
if end < 0:
    end = content.find('\ndef ', idx + 10)
func = content[idx:end]

# Replace the personal_summary line:
old_summary = "    optimized['个人总结'] = generate_personal_summary(sections, target_job, matched_key, competencies, supplements)"
new_summary = """    # 个人总结 - graceful degradation
    try:
        summary_result = generate_personal_summary(sections, target_job, matched_key, competencies, supplements)
        if summary_result.startswith('[AI生成失败'):
            optimized['个人总结'] = summary_result + '\\n\\n[说明：AI生成失败，你可以参考求职意向部分手动填写个人总结]'
        else:
            optimized['个人总结'] = summary_result
    except Exception as ex:
        optimized['个人总结'] = f'[生成失败: {str(ex)}]'"""

count2 = func.count(old_summary)
print('F2: personal_summary wrapping:', count2, 'found')
func = func.replace(old_summary, new_summary, 1)

# Replace the experience lines
old_exp1 = "        optimized['实习经历'] = optimize_experience(sections['实习经历'], target_job, competencies, supplements)"
new_exp1 = """        try:
            exp_result = optimize_experience(sections['实习经历'], target_job, competencies, supplements)
            optimized['实习经历'] = exp_result if not exp_result.startswith('[AI生成失败') else f'[部分内容生成失败] {exp_result}'
        except Exception as ex:
            optimized['实习经历'] = f'[生成失败: {str(ex)}]'"""

old_exp2 = "        optimized['项目经验'] = optimize_experience(sections['项目经验'], target_job, competencies, supplements)"
new_exp2 = """        try:
            proj_result = optimize_experience(sections['项目经验'], target_job, competencies, supplements)
            optimized['项目经验'] = proj_result if not proj_result.startswith('[AI生成失败') else f'[部分内容生成失败] {proj_result}'
        except Exception as ex:
            optimized['项目经验'] = f'[生成失败: {str(ex)}]'"""

old_skills = "        optimized['技能证书'] = optimize_skills(sections['技能证书'], target_job, competencies, supplements)"
new_skills = """        try:
            skills_result = optimize_skills(sections['技能证书'], target_job, competencies, supplements)
            optimized['技能证书'] = skills_result if not skills_result.startswith('[AI生成失败') else f'[部分内容生成失败] {skills_result}'
        except Exception as ex:
            optimized['技能证书'] = f'[生成失败: {str(ex)}]'"""

count3 = func.count(old_exp1)
count4 = func.count(old_exp2)
count5 = func.count(old_skills)
print(f'F2: exp1:{count3} exp2:{count4} skills:{count5} found')

func = func.replace(old_exp1, new_exp1, 1)
func = func.replace(old_exp2, new_exp2, 1)
func = func.replace(old_skills, new_skills, 1)

# Reassemble
content = content[:idx] + func + content[end:]

# === FIX 3: /api/optimize route - wrap whole generate_optimized_resume call ===
# Find the optimize_resume function
idx2 = content.find('def optimize_resume(')
end2 = content.find('\n@app.route', idx2)
if end2 < 0:
    end2 = len(content)
route_func = content[idx2:end2]

# Add try-except around the generate_optimized_resume call
old_opt_call = '''    optimized = generate_optimized_resume(sections, target_job, matched_key, supplements)

    

    # AI 生成个性化面试话术(如果没有提供职业信息)'''

new_opt_call = '''    try:
        optimized = generate_optimized_resume(sections, target_job, matched_key, supplements)
    except Exception as e:
        optimized = {'_error': str(e), '_original_sections': sections, '_target_job': target_job, '_career_key': matched_key}
        optimized['求职意向'] = f'**目标岗位：{target_job}**\\n**期望城市：** 待补充\\n**到岗时间：** 一周内'

    # AI 生成个性化面试话术'''

count6 = route_func.count(old_opt_call)
print(f'F3: optimize try-except: {count6} found')
route_func = route_func.replace(old_opt_call, new_opt_call, 1)

content = content[:idx2] + route_func + content[end2:]

# === FIX 4: Optimize route - always return JSON even on error ===
# Make sure jsonify at the end returns the error too
old_return = '''    return jsonify({
        **optimized,
        "interview_ai": interview_ai
    })'''

new_return = '''    response_data = {
        **optimized,
        "interview_ai": interview_ai
    }
    return jsonify(response_data)'''

# Only replace if the old pattern exists
if old_return in route_func:
    route_func2 = content[idx2:idx2+len(route_func)]
    route_func2 = route_func2.replace(old_return, new_return, 1)
    content = content[:idx2] + route_func2 + content[idx2+len(route_func):]
    print('F4: jsonify response updated')
else:
    print('F4: pattern not found, skipping')

# Verify syntax
import ast
try:
    ast.parse(content)
    print('Syntax check: OK')
except SyntaxError as e:
    print('SYNTAX ERROR:', e)
    content = original  # revert

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
print('AI timeout now:', new)
print('Total replacements:', count + count2 + count3 + count4 + count5)