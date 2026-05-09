# -*- coding: utf-8 -*-
"""Patch app.py to support text upload and supplements in optimization"""
import re

path = r"C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Update generate_optimized_resume signature and body
old1 = '''def generate_optimized_resume(sections, target_job, career_key):

    """根据目标岗位生成优化后的简历"""
    matched_key, career_info = match_career_info(target_job)
    if not matched_key:
        matched_key = career_key
        career_info = CAREER_DB.get(career_key)
    
    competencies = career_info.get("competencies", []) if career_info else []
    
    optimized = {}
    
    # === 优化求职意向 ===
    if '求职意向' in sections:
        original = sections['求职意向']
        optimized['求职意向'] = f"""**目标岗位：{target_job}**
**期望城市：** 北京
**期望薪资：** 面议
**到岗时间：** 一周内


> 聚焦{matched_key or target_job}方向，具备{', '.join(competencies[:3])}等核心能力，
> 寻求能在实践中快速成长、为公司创造真实价值的平台。"""
    else:
        optimized['求职意向'] = f"""**目标岗位：{target_job}**
**期望城市：** 北京
**期望薪资：** 面议
**到岗时间：** 一周内"""
    
    # === 优化个人总结/自我评价 ===
    all_text = '\\n'.join(sections.values())
    optimized['个人总结'] = generate_personal_summary(sections, target_job, matched_key, competencies)
    
    # === 优化实习经历 ===
    if '实习经历' in sections:
        optimized['实习经历'] = optimize_experience(sections['实习经历'], target_job, competencies)
    
    # === 优化项目经验 ===
    if '项目经验' in sections:
        optimized['项目经验'] = optimize_experience(sections['项目经验'], target_job, competencies)
    
    # === 优化技能 ===
    if '技能证书' in sections:
        optimized['技能证书'] = optimize_skills(sections['技能证书'], target_job, competencies)
    
    # === 优化教育经历 ===
    if '教育经历' in sections:
        optimized['教育经历'] = sections['教育经历']
    
    # 原始内容保留
    optimized['_original_sections'] = sections
    optimized['_target_job'] = target_job
    optimized['_career_key'] = matched_key
    
    return optimized'''

new1 = '''def generate_optimized_resume(sections, target_job, career_key, supplements=None):

    """根据目标岗位生成优化后的简历，supplements是用户补充的经历 dict{keyword: text}"""
    matched_key, career_info = match_career_info(target_job)
    if not matched_key:
        matched_key = career_key
        career_info = CAREER_DB.get(career_key)

    competencies = career_info.get("competencies", []) if career_info else []

    optimized = {}

    # === 优化求职意向 ===
    if '求职意向' in sections:
        original = sections['求职意向']
        optimized['求职意向'] = f"""**目标岗位：{target_job}**
**期望城市：** 北京
**期望薪资：** 面议
**到岗时间：** 一周内

> 聚焦{matched_key or target_job}方向，具备{', '.join(competencies[:3])}等核心能力，
> 寻求能在实践中快速成长、为公司创造真实价值的平台。"""
    else:
        optimized['求职意向'] = f"""**目标岗位：{target_job}**
**期望城市：** 北京
**期望薪资：** 面议
**到岗时间：** 一周内"""

    # === 优化个人总结/自我评价 ===
    all_text = '\\n'.join(sections.values())
    optimized['个人总结'] = generate_personal_summary(sections, target_job, matched_key, competencies, supplements)

    # === 优化实习经历 ===
    if '实习经历' in sections:
        optimized['实习经历'] = optimize_experience(sections['实习经历'], target_job, competencies, supplements)

    # === 优化项目经验 ===
    if '项目经验' in sections:
        optimized['项目经验'] = optimize_experience(sections['项目经验'], target_job, competencies, supplements)

    # === 优化技能 ===
    if '技能证书' in sections:
        optimized['技能证书'] = optimize_skills(sections['技能证书'], target_job, competencies)

    # === 优化教育经历 ===
    if '教育经历' in sections:
        optimized['教育经历'] = sections['教育经历']

    # 原始内容保留
    optimized['_original_sections'] = sections
    optimized['_target_job'] = target_job
    optimized['_career_key'] = matched_key

    return optimized'''

if old1 in content:
    content = content.replace(old1, new1)
    print("✅ generate_optimized_resume patched")
else:
    print("⚠️  generate_optimized_resume pattern not found exactly")

# Fix 2: Update generate_personal_summary
old2 = '''def generate_personal_summary(sections, target_job, career_key, competencies):
    """用 AI 生成针对性的个人总结"""
    edu = sections.get('教育经历', '')
    exp = sections.get('实习经历', '')
    project = sections.get('项目经验', '')
    skills = sections.get('技能证书', '')
    eval_text = sections.get('自我评价', '')
    
    comp_str = '、'.join(competencies[:5]) if competencies else '运营、策划、数据分析'
    exp_desc = exp if exp else (project if project else '暂无实习/项目经历')
    
    prompt = f"你是一个专业的简历优化顾问。请根据以下简历内容，为一个应聘【{target_job}】岗位的应届生/实习生写一段专业的个人总结(150字以内)。要求：1) 第一人称，简洁有力 2) 突出与{target_job}岗位相关的经历和能力 3) 融入岗位关键词 4) 不要空洞套话，要具体信息点 5) 直接输出，不要加标题\\n简历信息：教育：{edu[:200]} 实习/项目：{exp_desc[:300]} 技能：{skills[:200]} 自我评价：{eval_text[:200] if eval_text else '无'}\\n直接输出："

    result = call_ai(prompt, max_tokens=500, temperature=0.7)
    return f"### 个人总结\\n\\n{result}"'''

new2 = '''def generate_personal_summary(sections, target_job, career_key, competencies, supplements=None):
    """用 AI 生成针对性的个人总结，supplements为用户补充的经历"""
    edu = sections.get('教育经历', '')
    exp = sections.get('实习经历', '')
    project = sections.get('项目经验', '')
    skills = sections.get('技能证书', '')
    eval_text = sections.get('自我评价', '')

    comp_str = '、'.join(competencies[:5]) if competencies else '运营、策划、数据分析'
    exp_desc = exp if exp else (project if project else '暂无实习/项目经历')

    supp_str = ''
    if supplements:
        supp_parts = [f"【{k}相关经历】：{v}" for k, v in supplements.items() if v]
        if supp_parts:
            supp_str = '\\n'.join(supp_parts)

    prompt = (
        f"你是一个专业的简历优化顾问。请根据以下简历内容，为一个应聘【{target_job}】岗位的候选人写一段专业的个人总结(150字以内)。"
        f"要求：1) 第一人称，简洁有力 2) 突出与{target_job}岗位相关的经历和能力 3) 融入岗位关键词 4) 不要空洞套话，要具体信息点 5) 直接输出，不要加标题\\n"
        f"简历信息：\\n教育：{edu[:200]}\\n实习/项目：{exp_desc[:300]}\\n技能：{skills[:200]}\\n自我评价：{eval_text[:200] if eval_text else '无'}\\n"
        + (f"\\n用户补充的经历（请重点融入）：\\n{supp_str}\\n" if supp_str else "")
        + f"\\n直接输出："
    )

    result = call_ai(prompt, max_tokens=500, temperature=0.7)
    return f"### 个人总结\\n\\n{result}"'''

if old2 in content:
    content = content.replace(old2, new2)
    print("✅ generate_personal_summary patched")
else:
    print("⚠️  generate_personal_summary pattern not found exactly")

# Fix 3: Update optimize_experience
old3 = '''def optimize_experience(original_exp, target_job, competencies):
    """用 AI 优化实习/项目经历描述"""
    comp_str = '、'.join(competencies[:5]) if competencies else '运营、策划、数据分析'
    prompt = f"你是一个资深HR。请将以下实习/项目经历用STAR法则优化重写，使其更专业、更有针对性。要求：1)STAR结构(情境-任务-行动-结果)2)动词开头：负责、主导、推进、优化、搭建、分析等 3)量化成果，加具体数字 4)融入关键词：{comp_str} 5)每条2-4行 6)直接输出不加说明\\n原始内容：{original_exp}\\n优化后："

    result = call_ai(prompt, max_tokens=1200, temperature=0.7)
    return result'''

new3 = '''def optimize_experience(original_exp, target_job, competencies, supplements=None):
    """用 AI 优化实习/项目经历描述，supplements为用户补充的经历"""
    comp_str = '、'.join(competencies[:5]) if competencies else '运营、策划、数据分析'

    supp_str = ''
    if supplements:
        supp_parts = [f"【{k}相关经历】：{v}" for k, v in supplements.items() if v]
        if supp_parts:
            supp_str = '\\n'.join(supp_parts)

    prompt = (
        f"你是一个资深HR。请将以下实习/项目经历用STAR法则优化重写，使其更专业、更有针对性。"
        f"要求：1)STAR结构(情境-任务-行动-结果)2)动词开头：负责、主导、推进、优化、搭建、分析等 3)量化成果，加具体数字 "
        f"4)融入关键词：{comp_str} 5)每条2-4行 6)直接输出不加说明\\n"
        + (f"\\n用户补充的相关经历（请重点融入到描述中）：\\n{supp_str}\\n" if supp_str else "")
        + f"原始内容：{original_exp}\\n优化后："
    )

    result = call_ai(prompt, max_tokens=1200, temperature=0.7)
    return result'''

if old3 in content:
    content = content.replace(old3, new3)
    print("✅ optimize_experience patched")
else:
    print("⚠️  optimize_experience pattern not found exactly")

# Fix 4: Update optimize_resume route to pass supplements
old4 = '''    optimized = generate_optimized_resume(sections, target_job, matched_key)'''

new4 = '''    supplements = data.get('supplements', {})
    optimized = generate_optimized_resume(sections, target_job, matched_key, supplements)'''

if old4 in content:
    content = content.replace(old4, new4)
    print("✅ optimize route patched (supplements)")
else:
    print("⚠️  optimize route pattern not found exactly")

# Fix 5: Add text-upload route before upload route
old5 = '''@app.route('/api/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "请上传PDF简历文件"}), 400'''

new5 = '''@app.route('/api/text-upload', methods=['POST'])
def text_upload():
    """文字输入简历解析"""
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


@app.route('/api/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "请上传PDF简历文件"}), 400'''

if old5 in content:
    content = content.replace(old5, new5)
    print("✅ text-upload route added")
else:
    print("⚠️  text-upload route insertion point not found")

# Write back
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ All patches applied!")
