# -*- coding: utf-8 -*-
filepath = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(filepath, 'rb') as f:
    content = f.read()

idx = content.find(b'def diagnose_resume(')
next_def = content.find(b'\ndef ', idx + 10)
old_func = content[idx:next_def].decode('utf-8')

new_func = '''def diagnose_resume(sections, target_job=""):
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

content_str = content.decode('utf-8')
content_str = content_str.replace(old_func, new_func)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content_str)

print('OK: diagnose_resume has try-except now')
