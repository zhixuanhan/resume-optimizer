# -*- coding: utf-8 -*-
"""
给 career_analysis 路由加 try-except 异常保护
"""
filepath = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(filepath, 'rb') as f:
    content = f.read()

s = content.decode('utf-8')

old = '''def career_analysis():

    data = request.json

    session_id = data.get('session_id')

    target_job = data.get('target_job', '')

    

    session_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.json")

    if not os.path.exists(session_file):

        return jsonify({"error": "会话不存在"}), 400

    

    with open(session_file, 'r', encoding='utf-8') as f:

        session_data = json.load(f)

    

    sections = session_data.get('sections', {})

    all_text = '\\n'.join(f"【{k}】\\n{sections[k]}" for k in sections if sections.get(k))

    

    matched_key, career_info = match_career_info(target_job)

    

    if not career_info:

        return jsonify({

            "error": f"暂无「{target_job}」的详细数据，支持的岗位：{', '.join(CAREER_DB.keys())}",

            "available_jobs": list(CAREER_DB.keys())

        }), 404'''

new = '''def career_analysis():
    try:
        data = request.json
        session_id = data.get('session_id')
        target_job = data.get('target_job', '')
        session_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.json")
        if not os.path.exists(session_file):
            return jsonify({"error": "会话不存在"}), 400
        with open(session_file, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        sections = session_data.get('sections', {})
        all_text = '\\n'.join(f"【{k}】\\n{sections[k]}" for k in sections if sections.get(k))
        matched_key, career_info = match_career_info(target_job)
        if not career_info:
            return jsonify({
                "error": f"暂无「{target_job}」的详细数据，支持的岗位：{', '.join(CAREER_DB.keys())}",
                "available_jobs": list(CAREER_DB.keys())
            }), 404'''

if old in s:
    s = s.replace(old, new)
    
    # 现在需要在函数结尾加 except，找到 return jsonify({  (career_analysis 的最终返回)
    # 找到 career_analysis 函数的末尾 - 下一个 @app.route 或 def 开头
    start = s.find('def career_analysis():')
    # 找函数结尾 - 下一个顶层 def 或 @app.route
    next_route = s.find('\n@app.route', start)
    next_def = s.find('\ndef ', start + 10)
    end_candidates = [x for x in [next_route, next_def] if x > start]
    if end_candidates:
        func_end = min(end_candidates)
        # 检查是否已经有 except
        func_body = s[start:func_end]
        if 'except Exception' not in func_body:
            # 在最后一个 return 前插入 except
            last_return = func_body.rfind('\n    return ')
            if last_return > 0:
                indent = '    '
                except_block = indent + '''except Exception as e:
                import traceback
                traceback.print_exc()
                return jsonify({"error": f"职业分析失败: {str(e)[:80]}", "match_score": 30, "matched_keywords": [], "missing_keywords": [], "transferable_skills": [], "career_advice": "分析出错，请重试"})'''
                s = s[:start + last_return] + except_block + '\n' + s[start + last_return:]
                print("Added except to career_analysis")
else:
    print("WARNING: Could not find career_analysis pattern")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(s)

print("Done")
