# -*- coding: utf-8 -*-
"""Patch app.py - normalize CRLF, apply patches"""
path = r"C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py"
with open(path, 'rb') as f:
    raw = f.read()
content = raw.replace(b'\r\n', b'\n').decode('utf-8')

results = []

# Patch 1: add text-upload route BEFORE /api/upload
old5 = "@app.route('/api/upload', methods=['POST'])\ndef upload_resume():\n    if 'resume' not in request.files:"
new5 = """@app.route('/api/text-upload', methods=['POST'])
def text_upload():
    \"\"\"文字输入简历解析\"\"\"
    data = request.json
    text = data.get('text', '')
    text = text.strip()
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


@app.route('/api/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:"""
if old5 in content:
    content = content.replace(old5, new5)
    results.append("OK: text-upload route added")
else:
    results.append("SKIP: text-upload route point not found")

# Patch 2: generate_optimized_resume signature
old1 = "def generate_optimized_resume(sections, target_job, career_key):\n    \"\"\"根据目标岗位生成优化后的简历\"\"\""
new1 = "def generate_optimized_resume(sections, target_job, career_key, supplements=None):\n    \"\"\"根据目标岗位生成优化后的简历，supplements是用户补充的经历 dict{keyword: text}\"\"\""
if old1 in content:
    content = content.replace(old1, new1)
    results.append("OK: generate_optimized_resume signature patched")
else:
    results.append("SKIP: generate_optimized_resume signature not found")

# Update calls to generate_personal_summary inside generate_optimized_resume
old1b = "    optimized['个人总结'] = generate_personal_summary(sections, target_job, matched_key, competencies)"
new1b = "    optimized['个人总结'] = generate_personal_summary(sections, target_job, matched_key, competencies, supplements)"
if old1b in content:
    content = content.replace(old1b, new1b)
    results.append("OK: generate_personal_summary call patched")
else:
    results.append("SKIP: generate_personal_summary call not found")

# Update calls to optimize_experience inside generate_optimized_resume
old1c = "        optimized['实习经历'] = optimize_experience(sections['实习经历'], target_job, competencies)\n    \n    # === 优化项目经验 ===\n    if '项目经验' in sections:\n        optimized['项目经验'] = optimize_experience(sections['项目经验'], target_job, competencies)"
new1c = "        optimized['实习经历'] = optimize_experience(sections['实习经历'], target_job, competencies, supplements)\n    \n    # === 优化项目经验 ===\n    if '项目经验' in sections:\n        optimized['项目经验'] = optimize_experience(sections['项目经验'], target_job, competencies, supplements)"
if old1c in content:
    content = content.replace(old1c, new1c)
    results.append("OK: optimize_experience calls patched")
else:
    results.append("SKIP: optimize_experience calls not found")

# Patch 3: generate_personal_summary signature
old2 = 'def generate_personal_summary(sections, target_job, career_key, competencies):\n    """用 AI 生成针对性的个人总结"""'
new2 = 'def generate_personal_summary(sections, target_job, career_key, competencies, supplements=None):\n    """用 AI 生成针对性的个人总结，supplements为用户补充的经历"""'
if old2 in content:
    content = content.replace(old2, new2)
    results.append("OK: generate_personal_summary signature patched")
else:
    results.append("SKIP: generate_personal_summary signature not found")

# Patch generate_personal_summary prompt: add supp_str and update prompt
old2_prompt = '    prompt = f"你是一个专业的简历优化顾问。请根据以下简历内容，为一个应聘【{target_job}】岗位的应届生/实习生写一段专业的个人总结(150字以内)。要求：1) 第一人称，简洁有力 2) 突出与{target_job}岗位相关的经历和能力 3) 融入岗位关键词 4) 不要空洞套话，要具体信息点 5) 直接输出，不要加标题\\\\n简历信息：教育：{edu[:200]} 实习/项目：{exp_desc[:300]} 技能：{skills[:200]} 自我评价：{eval_text[:200] if eval_text else \'无\'}\\\\n直接输出："'
new2_prompt = '    supp_str = \'\'\n    if supplements:\n        supp_parts = [f"【{k}相关经历】：{v}" for k, v in supplements.items() if v]\n        if supp_parts:\n            supp_str = \'\\n\'.join(supp_parts)\n\n    prompt = (\n        f"你是一个专业的简历优化顾问。请根据以下简历内容，为一个应聘【{target_job}】岗位的候选人写一段专业的个人总结(150字以内)。"\n        f"要求：1) 第一人称，简洁有力 2) 突出与{target_job}岗位相关的经历和能力 3) 融入岗位关键词 4) 不要空洞套话，要具体信息点 5) 直接输出，不要加标题\\\\n"\n        f"简历信息：\\n教育：{edu[:200]}\\n实习/项目：{exp_desc[:300]}\\n技能：{skills[:200]}\\n自我评价：{eval_text[:200] if eval_text else \'无\'}\\n"\n        + (f"\\n用户补充的经历（请重点融入）：\\n{supp_str}\\n" if False else "")\n        + f"\\n直接输出："\n    )'
if old2_prompt in content:
    content = content.replace(old2_prompt, new2_prompt)
    results.append("OK: generate_personal_summary prompt patched")
else:
    results.append("SKIP: generate_personal_summary prompt not found")

# Patch 4: optimize_experience signature
old3 = 'def optimize_experience(original_exp, target_job, competencies):\n    """用 AI 优化实习/项目经历描述"""'
new3 = 'def optimize_experience(original_exp, target_job, competencies, supplements=None):\n    """用 AI 优化实习/项目经历描述，supplements为用户补充的经历"""'
if old3 in content:
    content = content.replace(old3, new3)
    results.append("OK: optimize_experience signature patched")
else:
    results.append("SKIP: optimize_experience signature not found")

# Patch optimize_experience prompt
old3_prompt = '    prompt = f"你是一个资深HR。请将以下实习/项目经历用STAR法则优化重写，使其更专业、更有针对性。要求：1)STAR结构(情境-任务-行动-结果)2)动词开头：负责、主导、推进、优化、搭建、分析等 3)量化成果，加具体数字 4)融入关键词：{comp_str} 5)每条2-4行 6)直接输出不加说明\\\\n原始内容：{original_exp}\\\\n优化后："'
new3_prompt = '    supp_str = \'\'\n    if supplements:\n        supp_parts = [f"【{k}相关经历】：{v}" for k, v in supplements.items() if v]\n        if supp_parts:\n            supp_str = \'\\n\'.join(supp_parts)\n\n    prompt = (\n        f"你是一个资深HR。请将以下实习/项目经历用STAR法则优化重写，使其更专业、更有针对性。"\n        f"要求：1)STAR结构(情境-任务-行动-结果)2)动词开头：负责、主导、推进、优化、搭建、分析等 3)量化成果，加具体数字 "\n        f"4)融入关键词：{comp_str} 5)每条2-4行 6)直接输出不加说明\\\\n"\n        + (f"\\n用户补充的相关经历（请重点融入到描述中）：\\n{supp_str}\\n" if False else "")\n        + f"原始内容：{original_exp}\\n优化后："\n    )'
if old3_prompt in content:
    content = content.replace(old3_prompt, new3_prompt)
    results.append("OK: optimize_experience prompt patched")
else:
    results.append("SKIP: optimize_experience prompt not found")

# Patch 5: optimize route pass supplements
old4 = '    optimized = generate_optimized_resume(sections, target_job, matched_key)'
new4 = '    supplements = data.get(\'supplements\', {})\n    optimized = generate_optimized_resume(sections, target_job, matched_key, supplements)'
if old4 in content:
    content = content.replace(old4, new4)
    results.append("OK: optimize route patched")
else:
    results.append("SKIP: optimize route not found")

# Write back with LF
with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

for r in results:
    print(r)
print("Done")
