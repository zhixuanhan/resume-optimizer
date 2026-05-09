# -*- coding: utf-8 -*-
"""
给 diagnose_resume 函数加 try-except 异常保护
"""

filepath = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''def diagnose_resume(sections, target_job=""):
    """用 AI 对简历进行诊断评分"""
    all_text = '\\n'.join(f"【{k}】\\n{sections[k]}" for k in sections if sections.get(k))
    prompt = (
        f"你是一位资深HR和猎头，请对以下简历进行评分(0-100分)和详细诊断。\\n\\n"
        f"目标岗位：{target_job or '未指定'}\\n\\n"
        f"简历内容：\\n{all_text[:3000]}\\n\\n"
        '请以详细JSON格式回复(只输出JSON，不要其他内容)：\\n'
        '{"score":分数,"good":["优点1","优点2"],"bad":["不足1","不足2"],"suggestions":["建议1","建议2"]}'
    )
    result = call_ai(prompt, max_tokens=800, temperature=0.3)
    parsed = extract_json(result)
    if parsed:
        return parsed
    return {"score": 50, "good": ["简历已上传"], "bad": ["诊断生成失败，请重试"], "suggestions": ["请检查网络后重试"]}'''

new_func = '''def diagnose_resume(sections, target_job=""):
    """用 AI 对简历进行诊断评分"""
    try:
        all_text = '\\n'.join(f"【{k}】\\n{sections[k]}" for k in sections if sections.get(k))
        prompt = (
            f"你是一位资深HR和猎头，请对以下简历进行评分(0-100分)和详细诊断。\\n\\n"
            f"目标岗位：{target_job or '未指定'}\\n\\n"
            f"简历内容：\\n{all_text[:3000]}\\n\\n"
            '请以详细JSON格式回复(只输出JSON，不要其他内容)：\\n'
            '{"score":分数,"good":["优点1","优点2"],"bad":["不足1","不足2"],"suggestions":["建议1","建议2"]}'
        )
        result = call_ai(prompt, max_tokens=800, temperature=0.3)
        parsed = extract_json(result)
        if parsed:
            return parsed
        return {"score": 50, "good": ["简历结构完整"], "bad": ["AI诊断解析失败，请重试"], "suggestions": ["可尝试重新上传或刷新页面"]}
    except Exception as e:
        return {"score": 50, "good": ["简历已上传"], "bad": [f"诊断失败: {str(e)[:50]}"], "suggestions": ["请检查网络后重试"]}'''

if old_func in content:
    content = content.replace(old_func, new_func)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK: diagnose_resume 已加异常保护")
else:
    print("WARN: 未找到目标函数，尝试模糊匹配...")
    # 尝试找函数开始位置
    idx = content.find('def diagnose_resume(')
    if idx >= 0:
        print(f"找到函数在位置 {idx}")
        print(content[idx:idx+100])
    else:
        print("ERROR: 完全找不到 diagnose_resume 函数")
