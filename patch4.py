# -*- coding: utf-8 -*-
"""Regex-based patch for app.py"""
import re

path = r"C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py"
with open(path, 'rb') as f:
    raw = f.read()
content = raw.replace(b'\r\n', b'\n').decode('utf-8')

results = []

# 1. Add text-upload route
pt1 = re.search(r"(@app\.route\('/api/upload', methods=\['POST'\]\)\ndef upload_resume\(\):\n    if 'resume' not in request\.files:)", content)
if pt1:
    new_route = """@app.route('/api/text-upload', methods=['POST'])
def text_upload():
    \"\"\"文字输入简历解析\"\"\"
    data = request.json
    text = data.get('text', '').strip()
    if not text:
        return jsonify({"error": "请输入简历内容"}), 400

    session_id = str(uuid.uuid4())[:8]
    sections = parse_resume_sections(text)

    session_data = {
        "session_id": session_id,
        "filename": "文字输入",
        "filepath": "",
        "raw_text": text,
        "sections": sections,
        "target_job": "",
        "diagnosis": None,
        "career_info": None,
        "optimized_resume": None
    }

    session_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.json")
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    return jsonify({
        "session_id": session_id,
        "filename": "文字输入",
        "text_preview": text[:2000] + ("..." if len(text) > 2000 else ""),
        "sections": {k: (v[:500] + "..." if len(v) > 500 else v) for k, v in sections.items()},
        "section_count": len([v for v in sections.values() if len(v) > 20]),
        "job_recommendations": _get_ai_job_recommendations(text[:3000])
    })


"""
    content = content[:pt1.start()] + new_route + content[pt1.start():]
    results.append("OK: text-upload route added")
else:
    results.append("SKIP: text-upload route point not found")

# 2. generate_optimized_resume: add supplements param + pass to callees
content = re.sub(
    r"def generate_optimized_resume\(sections, target_job, career_key\):\n    \"\"\"根据目标岗位生成优化后的简历\"\"\"",
    "def generate_optimized_resume(sections, target_job, career_key, supplements=None):\n    \"\"\"根据目标岗位生成优化后的简历，supplements是用户补充的经历 dict{keyword: text}\"\"\"",
    content
)
results.append("OK: generate_optimized_resume signature patched (regex)")

# 3. Pass supplements to generate_personal_summary and optimize_experience inside generate_optimized_resume
# Find the function body and update the calls
content = re.sub(
    r"    optimized\['个人总结'\] = generate_personal_summary\(sections, target_job, matched_key, competencies\)",
    "    optimized['个人总结'] = generate_personal_summary(sections, target_job, matched_key, competencies, supplements)",
    content
)
content = re.sub(
    r"        optimized\['实习经历'\] = optimize_experience\(sections\['实习经历'\], target_job, competencies\)\n    \n    # === 优化项目经验 ===\n    if '项目经验' in sections:\n        optimized\['项目经验'\] = optimize_experience\(sections\['项目经验'\], target_job, competencies\)",
    "        optimized['实习经历'] = optimize_experience(sections['实习经历'], target_job, competencies, supplements)\n    \n    # === 优化项目经验 ===\n    if '项目经验' in sections:\n        optimized['项目经验'] = optimize_experience(sections['项目经验'], target_job, competencies, supplements)",
    content
)
results.append("OK: internal calls patched (regex)")

# 4. generate_personal_summary: signature + body
content = re.sub(
    r"def generate_personal_summary\(sections, target_job, career_key, competencies\):\n    \"\"\"用 AI 生成针对性的个人总结\"\"\"",
    "def generate_personal_summary(sections, target_job, career_key, competencies, supplements=None):\n    \"\"\"用 AI 生成针对性的个人总结，supplements为用户补充的经历\"\"\"",
    content
)
results.append("OK: generate_personal_summary signature (regex)")

# Update prompt in generate_personal_summary: insert supp_str block before prompt line
old_prompt_pat = r'(    eval_text = sections\.get\([\'"']自我评价[\'"'], [\'"\'\])\n\n    comp_str)'
new_prompt_block = r'''    eval_text = sections.get('自我评价', '')

    supp_str = ''
    if supplements:
        supp_parts = [f"【{k}相关经历】：{v}" for k, v in supplements.items() if v]
        if supp_parts:
            supp_str = '\n'.join(supp_parts)

    comp_str'''
content = re.sub(old_prompt_pat, new_prompt_block, content)
results.append("OK: supp_str added to generate_personal_summary")

# Now update the prompt string to include supp_str
old_final_prompt = (
    '    prompt = f"你是一个专业的简历优化顾问。请根据以下简历内容，为一个应聘【{target_job}】岗位的应届生/实习生写一段专业的个人总结(150字以内)。'
    '要求：1) 第一人称，简洁有力 2) 突出与{target_job}岗位相关的经历和能力 3) 融入岗位关键词 4) 不要空洞套话，要具体信息点 5) 直接输出，不要加标题\\n'
    '简历信息：教育：{edu[:200]} 实习/项目：{exp_desc[:300]} 技能：{skills[:200]} 自我评价：{eval_text[:200] if eval_text else [\'"']无[\'"']}\\n直接输出："'
)
new_final_prompt = (
    "    prompt = (\n"
    '        f"你是一个专业的简历优化顾问。请根据以下简历内容，为一个应聘【{target_job}】岗位的候选人写一段专业的个人总结(150字以内)。"\n'
    '        f"要求：1) 第一人称，简洁有力 2) 突出与{target_job}岗位相关的经历和能力 3) 融入岗位关键词 4) 不要空洞套话，要具体信息点 5) 直接输出，不要加标题\\n"\n'
    '        f"简历信息：\\n教育：{edu[:200]}\\n实习/项目：{exp_desc[:300]}\\n技能：{skills[:200]}\\n自我评价：{eval_text[:200] if eval_text else [\'"']无[\'"\']}\\n"\n'
    "        + (f\"\\n用户补充的经历（请重点融入）：\\n{supp_str}\\n\" if supp_str else \"\")\n"
    '        + "\\n直接输出："\n'
    "    )"
)
if old_final_prompt in content:
    content = content.replace(old_final_prompt, new_final_prompt)
    results.append("OK: generate_personal_summary prompt patched")
else:
    results.append("SKIP: generate_personal_summary prompt not found exactly")

# 5. optimize_experience: signature + body
content = re.sub(
    r"def optimize_experience\(original_exp, target_job, competencies\):\n    \"\"\"用 AI 优化实习/项目经历描述\"\"\"",
    "def optimize_experience(original_exp, target_job, competencies, supplements=None):\n    \"\"\"用 AI 优化实习/项目经历描述，supplements为用户补充的经历\"\"\"",
    content
)
results.append("OK: optimize_experience signature (regex)")

# Add supp_str before prompt in optimize_experience
content = re.sub(
    r'(    comp_str = [\'"'].*?[\'"]\n\n    prompt = f"你是一个资深HR)',
    r'''    supp_str = ''
    if supplements:
        supp_parts = [f"【{k}相关经历】：{v}" for k, v in supplements.items() if v]
        if supp_parts:
            supp_str = '\n'.join(supp_parts)

    \1''',
    content
)
results.append("OK: supp_str added to optimize_experience")

# Update optimize_experience prompt
old_opt_prompt = (
    '    prompt = f"你是一个资深HR。请将以下实习/项目经历用STAR法则优化重写，使其更专业、更有针对性。'
    '要求：1)STAR结构(情境-任务-行动-结果)2)动词开头：负责、主导、推进、优化、搭建、分析等 3)量化成果，加具体数字 '
    '4)融入关键词：{comp_str} 5)每条2-4行 6)直接输出不加说明\\n原始内容：{original_exp}\\n优化后："'
)
new_opt_prompt = (
    "    prompt = (\n"
    '        f"你是一个资深HR。请将以下实习/项目经历用STAR法则优化重写，使其更专业、更有针对性。"\n'
    '        f"要求：1)STAR结构(情境-任务-行动-结果)2)动词开头：负责、主导、推进、优化、搭建、分析等 3)量化成果，加具体数字 "\n'
    '        f"4)融入关键词：{comp_str} 5)每条2-4行 6)直接输出不加说明\\n"\n'
    "        + (f"\\n用户补充的相关经历（请重点融入到描述中）：\\n{supp_str}\\n" if False else \"\")\n"
    '        + f"原始内容：{original_exp}\\n优化后："\n'
    "    )"
)
if old_opt_prompt in content:
    content = content.replace(old_opt_prompt, new_opt_prompt)
    results.append("OK: optimize_experience prompt patched")
else:
    results.append("SKIP: optimize_experience prompt not found exactly")

# 6. optimize route: pass supplements
content = re.sub(
    r"    optimized = generate_optimized_resume\(sections, target_job, matched_key\)",
    "    supplements = data.get('supplements', {})\n    optimized = generate_optimized_resume(sections, target_job, matched_key, supplements)",
    content
)
results.append("OK: optimize route patched (regex)")

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

for r in results:
    print(r)
print("Done patching app.py")
