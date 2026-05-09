# -*- coding: utf-8 -*-
"""Patch app.py - ASCII safe"""
import re

path = r"C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

patches_applied = []

# Fix 1
old1 = 'def generate_optimized_resume(sections, target_job, career_key):\n\n    """根据目标岗位生成优化后的简历"""\n    matched_key, career_info = match_career_info(target_job)\n    if not matched_key:\n        matched_key = career_key\n        career_info = CAREER_DB.get(career_key)\n    \n    competencies = career_info.get("competencies", []) if career_info else []\n    \n    optimized = {}\n    \n    # === 优化求职意向 ===\n    if \'求职意向\' in sections:\n        original = sections[\'求职意向\']\n        optimized[\'求职意向\'] = f"""**目标岗位：{target_job}**\n**期望城市：** 北京\n**期望薪资：** 面议\n**到岗时间：** 一周内\n\n\n> 聚焦{matched_key or target_job}方向，具备{\', \'.join(competencies[:3])}等核心能力，\n> 寻求能在实践中快速成长、为公司创造真实价值的平台。"""\n    else:\n        optimized[\'求职意向\'] = f"""**目标岗位：{target_job}**\n**期望城市：** 北京\n**期望薪资：** 面议\n**到岗时间：** 一周内"""\n    \n    # === 优化个人总结/自我评价 ===\n    all_text = \'\\n\'.join(sections.values())\n    optimized[\'个人总结\'] = generate_personal_summary(sections, target_job, matched_key, competencies)\n    \n    # === 优化实习经历 ===\n    if \'实习经历\' in sections:\n        optimized[\'实习经历\'] = optimize_experience(sections[\'实习经历\'], target_job, competencies)\n    \n    # === 优化项目经验 ===\n    if \'项目经验\' in sections:\n        optimized[\'项目经验\'] = optimize_experience(sections[\'项目经验\'], target_job, competencies)\n    \n    # === 优化技能 ===\n    if \'技能证书\' in sections:\n        optimized[\'技能证书\'] = optimize_skills(sections[\'技能证书\'], target_job, competencies)\n    \n    # === 优化教育经历 ===\n    if \'教育经历\' in sections:\n        optimized[\'教育经历\'] = sections[\'教育经历\']\n    \n    # 原始内容保留\n    optimized[\'_original_sections\'] = sections\n    optimized[\'_target_job\'] = target_job\n    optimized[\'_career_key\'] = matched_key\n    \n    return optimized'
new1 = 'def generate_optimized_resume(sections, target_job, career_key, supplements=None):\n\n    """根据目标岗位生成优化后的简历，supplements是用户补充的经历 dict{keyword: text}"""\n    matched_key, career_info = match_career_info(target_job)\n    if not matched_key:\n        matched_key = career_key\n        career_info = CAREER_DB.get(career_key)\n\n    competencies = career_info.get("competencies", []) if career_info else []\n\n    optimized = {}\n\n    # === 优化求职意向 ===\n    if \'求职意向\' in sections:\n        original = sections[\'求职意向\']\n        optimized[\'求职意向\'] = f"""**目标岗位：{target_job}**\n**期望城市：** 北京\n**期望薪资：** 面议\n**到岗时间：** 一周内\n\n> 聚焦{matched_key or target_job}方向，具备{\', \'.join(competencies[:3])}等核心能力，\n> 寻求能在实践中快速成长、为公司创造真实价值的平台。"""\n    else:\n        optimized[\'求职意向\'] = f"""**目标岗位：{target_job}**\n**期望城市：** 北京\n**期望薪资：** 面议\n**到岗时间：** 一周内"""\n\n    # === 优化个人总结/自我评价 ===\n    all_text = \'\\n\'.join(sections.values())\n    optimized[\'个人总结\'] = generate_personal_summary(sections, target_job, matched_key, competencies, supplements)\n\n    # === 优化实习经历 ===\n    if \'实习经历\' in sections:\n        optimized[\'实习经历\'] = optimize_experience(sections[\'实习经历\'], target_job, competencies, supplements)\n\n    # === 优化项目经验 ===\n    if \'项目经验\' in sections:\n        optimized[\'项目经验\'] = optimize_experience(sections[\'项目经验\'], target_job, competencies, supplements)\n\n    # === 优化技能 ===\n    if \'技能证书\' in sections:\n        optimized[\'技能证书\'] = optimize_skills(sections[\'技能证书\'], target_job, competencies)\n\n    # === 优化教育经历 ===\n    if \'教育经历\' in sections:\n        optimized[\'教育经历\'] = sections[\'教育经历\']\n\n    # 原始内容保留\n    optimized[\'_original_sections\'] = sections\n    optimized[\'_target_job\'] = target_job\n    optimized[\'_career_key\'] = matched_key\n\n    return optimized'

if old1 in content:
    content = content.replace(old1, new1)
    patches_applied.append("OK generate_optimized_resume")
else:
    patches_applied.append("SKIP generate_optimized_resume (no match)")

# Fix 2
old2 = 'def generate_personal_summary(sections, target_job, career_key, competencies):\n    """用 AI 生成针对性的个人总结"""\n    edu = sections.get(\'教育经历\', \'\')\n    exp = sections.get(\'实习经历\', \'\')\n    project = sections.get(\'项目经验\', \'\')\n    skills = sections.get(\'技能证书\', \'\')\n    eval_text = sections.get(\'自我评价\', \'\')\n    \n    comp_str = \'、\'.join(competencies[:5]) if competencies else \'运营、策划、数据分析\'\n    exp_desc = exp if exp else (project if project else \'暂无实习/项目经历\')\n    \n    prompt = f"你是一个专业的简历优化顾问。请根据以下简历内容，为一个应聘【{target_job}】岗位的应届生/实习生写一段专业的个人总结(150字以内)。要求：1) 第一人称，简洁有力 2) 突出与{target_job}岗位相关的经历和能力 3) 融入岗位关键词 4) 不要空洞套话，要具体信息点 5) 直接输出，不要加标题\\n简历信息：教育：{edu[:200]} 实习/项目：{exp_desc[:300]} 技能：{skills[:200]} 自我评价：{eval_text[:200] if eval_text else \'无\'}\\n直接输出："\n\n    result = call_ai(prompt, max_tokens=500, temperature=0.7)\n    return f"### 个人总结\\n\\n{result}"'

new2 = 'def generate_personal_summary(sections, target_job, career_key, competencies, supplements=None):\n    """用 AI 生成针对性的个人总结，supplements为用户补充的经历"""\n    edu = sections.get(\'教育经历\', \'\')\n    exp = sections.get(\'实习经历\', \'\')\n    project = sections.get(\'项目经验\', \'\')\n    skills = sections.get(\'技能证书\', \'\')\n    eval_text = sections.get(\'自我评价\', \'\')\n\n    comp_str = \'、\'.join(competencies[:5]) if competencies else \'运营、策划、数据分析\'\n    exp_desc = exp if exp else (project if project else \'暂无实习/项目经历\')\n\n    supp_str = \'\'\n    if supplements:\n        supp_parts = [f"【{k}相关经历】：{v}" for k, v in supplements.items() if v]\n        if supp_parts:\n            supp_str = \'\\n\'.join(supp_parts)\n\n    prompt = (\n        f"你是一个专业的简历优化顾问。请根据以下简历内容，为一个应聘【{target_job}】岗位的候选人写一段专业的个人总结(150字以内)。"\n        f"要求：1) 第一人称，简洁有力 2) 突出与{target_job}岗位相关的经历和能力 3) 融入岗位关键词 4) 不要空洞套话，要具体信息点 5) 直接输出，不要加标题\\n"\n        f"简历信息：\\n教育：{edu[:200]}\\n实习/项目：{exp_desc[:300]}\\n技能：{skills[:200]}\\n自我评价：{eval_text[:200] if eval_text else \'无\'}\\n"\n        + (f"\\n用户补充的经历（请重点融入）：\\n{supp_str}\\n" if supp_str else "")\n        + f"\\n直接输出："\n    )\n\n    result = call_ai(prompt, max_tokens=500, temperature=0.7)\n    return f"### 个人总结\\n\\n{result}"'

if old2 in content:
    content = content.replace(old2, new2)
    patches_applied.append("OK generate_personal_summary")
else:
    patches_applied.append("SKIP generate_personal_summary (no match)")

# Fix 3
old3 = 'def optimize_experience(original_exp, target_job, competencies):\n    """用 AI 优化实习/项目经历描述"""\n    comp_str = \'、\'.join(competencies[:5]) if competencies else \'运营、策划、数据分析\'\n    prompt = f"你是一个资深HR。请将以下实习/项目经历用STAR法则优化重写，使其更专业、更有针对性。要求：1)STAR结构(情境-任务-行动-结果)2)动词开头：负责、主导、推进、优化、搭建、分析等 3)量化成果，加具体数字 4)融入关键词：{comp_str} 5)每条2-4行 6)直接输出不加说明\\n原始内容：{original_exp}\\n优化后："\n\n    result = call_ai(prompt, max_tokens=1200, temperature=0.7)\n    return result'

new3 = 'def optimize_experience(original_exp, target_job, competencies, supplements=None):\n    """用 AI 优化实习/项目经历描述，supplements为用户补充的经历"""\n    comp_str = \'、\'.join(competencies[:5]) if competencies else \'运营、策划、数据分析\'\n\n    supp_str = \'\'\n    if supplements:\n        supp_parts = [f"【{k}相关经历】：{v}" for k, v in supplements.items() if v]\n        if supp_parts:\n            supp_str = \'\\n\'.join(supp_parts)\n\n    prompt = (\n        f"你是一个资深HR。请将以下实习/项目经历用STAR法则优化重写，使其更专业、更有针对性。"\n        f"要求：1)STAR结构(情境-任务-行动-结果)2)动词开头：负责、主导、推进、优化、搭建、分析等 3)量化成果，加具体数字 "\n        f"4)融入关键词：{comp_str} 5)每条2-4行 6)直接输出不加说明\\n"\n        + (f"\\n用户补充的相关经历（请重点融入到描述中）：\\n{supp_str}\\n" if supp_str else "")\n        + f"原始内容：{original_exp}\\n优化后："\n    )\n\n    result = call_ai(prompt, max_tokens=1200, temperature=0.7)\n    return result'

if old3 in content:
    content = content.replace(old3, new3)
    patches_applied.append("OK optimize_experience")
else:
    patches_applied.append("SKIP optimize_experience (no match)")

# Fix 4: optimize route pass supplements
old4 = '    optimized = generate_optimized_resume(sections, target_job, matched_key)'
new4 = '    supplements = data.get(\'supplements\', {})\n    optimized = generate_optimized_resume(sections, target_job, matched_key, supplements)'
if old4 in content:
    content = content.replace(old4, new4)
    patches_applied.append("OK optimize route (supplements)")
else:
    patches_applied.append("SKIP optimize route (no match)")

# Fix 5: add text-upload route
old5 = '@app.route(\'/api/upload\', methods=[\'POST\'])\ndef upload_resume():\n    if \'resume\' not in request.files:'
new5 = '''@app.route(\'/api/text-upload\', methods=[\'POST\'])\ndef text_upload():\n    """文字输入简历解析"""\n    data = request.json\n    text = data.get(\'text\', \'\')\n    text = text.strip()\n    if not text:\n        return jsonify({"error": "请输入简历内容"}), 400\n\n    session_id = str(uuid.uuid4())[:8]\n    sections = parse_resume_sections(text)\n\n    session_data = {\n        "session_id": session_id,\n        "filename": "文字输入",\n        "filepath": "",\n        "raw_text": text,\n        "sections": sections,\n        "target_job": "",\n        "diagnosis": None,\n        "career_info": None,\n        "optimized_resume": None\n    }\n\n    session_file = os.path.join(app.config[\'UPLOAD_FOLDER\'], f"{session_id}.json")\n    with open(session_file, \'w\', encoding=\'utf-8\') as f:\n        json.dump(session_data, f, ensure_ascii=False, indent=2)\n\n    return jsonify({\n        "session_id": session_id,\n        "filename": "文字输入",\n        "text_preview": text[:2000] + ("..." if len(text) > 2000 else ""),\n        "sections": {k: (v[:500] + "..." if len(v) > 500 else v) for k, v in sections.items()},\n        "section_count": len([v for v in sections.values() if len(v) > 20]),\n        "job_recommendations": _get_ai_job_recommendations(text[:3000])\n    })\n\n\n@app.route(\'/api/upload\', methods=[\'POST\'])\ndef upload_resume():\n    if \'resume\' not in request.files:'''
if old5 in content:
    content = content.replace(old5, new5)
    patches_applied.append("OK text-upload route")
else:
    patches_applied.append("SKIP text-upload route (no match)")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

for p in patches_applied:
    print(p)
print("DONE")
