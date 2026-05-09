# -*- coding: utf-8 -*-
"""Fix app.py bugs"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# 1: add pdfplumber import after PyPDF2
old1 = 'from PyPDF2 import PdfReader\n\n\n# ====='
new1 = '''from PyPDF2 import PdfReader

# Try pdfplumber for better PDF parsing
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

# ====='''
if old1 in content:
    content = content.replace(old1, new1, 1)
    changes.append("import section ok")

# 2: replace extract_text_from_pdf
old2 = '''def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            pt = page.extract_text()
            if pt:
                text += pt + "\\n"
    except Exception as e:
        text = f"[PDF解析错误: {str(e)}]"
    return text.strip()'''

new2 = '''def extract_text_from_pdf(pdf_path):
    """Dual PDF parsing to maximize text extraction"""
    texts = []
    # Method 1: PyPDF2
    try:
        reader = PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            pt = page.extract_text()
            if pt and pt.strip():
                texts.append(f"[page{i+1}]\\n{pt}")
    except Exception:
        pass
    # Method 2: pdfplumber
    if HAS_PDFPLUMBER:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    t = page.extract_text()
                    if t and t.strip():
                        if t.strip() not in "\\n".join(texts):
                            texts.append(f"[page{i+1}]\\n{t}")
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            rows = [",".join([str(c or "").strip() for c in row]) for row in table if any(c for c in row)]
                            if rows:
                                texts.append("[table]\\n" + "\\n".join(rows))
        except Exception:
            pass
    if not texts:
        return "[PDF parse failed]"
    combined = "\\n".join(texts)
    combined = re.sub(r"[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f\\x7f-\\x9f]", "", combined)
    return combined.strip()'''

if old2 in content:
    content = content.replace(old2, new2, 1)
    changes.append("extract_text_from_pdf ok")
else:
    # try partial match
    idx = content.find("def extract_text_from_pdf")
    if idx >= 0:
        next_def = content.find("\\ndef ", idx + 10)
        if next_def > 0:
            content = content[:idx] + new2 + content[next_def:]
            changes.append("extract_text_from_pdf ok (partial)")

# 3: add extract_json before parse_resume_sections
extract_json_code = '''
def extract_json(s):
    """Extract JSON from AI response, handle markdown code blocks"""
    if not s:
        return None
    # Strip markdown code fences
    s = re.sub(r"^```(?:json)?\\s*", "", s.strip(), flags=re.IGNORECASE | re.MULTILINE)
    s = re.sub(r"\\s*```$", "", s.strip())
    start = s.find("{")
    end = s.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    raw = s[start:end+1]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    # Fix fullwidth quotes
    raw = raw.replace("\\u201c", '"').replace("\\u201d", '"').replace("\\u300c", '"').replace("\\u300d", '"')
    # Fix single-quote keys
    raw = re.sub(r"'([^']*?)'\\s*:", r'"\\1":', raw)
    # Fix single-quote values
    def fix_sq(m):
        inner = m.group(1).replace("\\\\\"", "[Q]").replace("'", "\\\\'").replace("[Q]", '"')
        return f'"{inner}"'
    raw = re.sub(r":\\s*'([^']*)'", fix_sq, raw)
    # Fix trailing commas
    raw = re.sub(r",\\s*([}\\]])", r"\\1", raw)
    try:
        return json.loads(raw)
    except:
        return None

'''
target3 = "\\ndef parse_resume_sections("
if target3 in content:
    content = content.replace(target3, extract_json_code + "def parse_resume_sections(", 1)
    changes.append("extract_json func ok")
else:
    # find by indent-free version
    idx = content.find("def parse_resume_sections(")
    if idx >= 0:
        content = content[:idx] + extract_json_code + content[idx:]
        changes.append("extract_json func ok (insert)")

# 4: diagnose_resume JSON parsing
old4 = '''    result = call_ai(prompt, max_tokens=800, temperature=0.3)
    try:
        # 尝试解析JSON
        start = result.find('{')
        end = result.rfind('}') + 1
        if start != -1 and end > start:
            return json.loads(result[start:end])
    except:
        pass
    # fallback
    return {"score": 50, "good": ["简历已上传"], "bad": ["诊断生成失败，请重试"], "suggestions": ["请检查网络后重试"]}'''

new4 = '''    result = call_ai(prompt, max_tokens=800, temperature=0.3)
    parsed = extract_json(result)
    if parsed:
        return parsed
    return {"score": 50, "good": ["简历已上传"], "bad": ["诊断生成失败，请重试"], "suggestions": ["请检查网络后重试"]}'''

if old4 in content:
    content = content.replace(old4, new4, 1)
    changes.append("diagnose_resume JSON ok")
else:
    # partial
    idx = content.find("def diagnose_resume(")
    if idx >= 0:
        fb = content.find('return {"score": 50', idx)
        if fb > 0:
            ai_line = content.find("result = call_ai", idx, fb)
            if ai_line > 0:
                # replace from ai_line to fallback return
                end_fb = fb + len('return {"score": 50, "good": ["简历已上传"], "bad": ["诊断生成失败，请重试"], "suggestions": ["请检查网络后重试"]}')
                content = content[:ai_line] + "    result = call_ai(prompt, max_tokens=800, temperature=0.3)\n    parsed = extract_json(result)\n    if parsed:\n        return parsed\n" + content[end_fb:]
                changes.append("diagnose_resume JSON ok (partial)")

# 5: career API JSON parsing
old5 = '''    ai_result = call_ai(ai_prompt, max_tokens=600, temperature=0.3)
    try:
        start = ai_result.find('{')
        end = ai_result.rfind('}') + 1
        ai_data = json.loads(ai_result[start:end]) if start != -1 and end > start else {}
    except:
        ai_data = {}'''

new5 = '''    ai_result = call_ai(ai_prompt, max_tokens=600, temperature=0.3)
    ai_data = extract_json(ai_result) or {}'''

if old5 in content:
    content = content.replace(old5, new5, 1)
    changes.append("career API JSON ok")
else:
    changes.append("career API: no change needed or partial")

# 6: job recommendations JSON
old6 = '''    result = call_ai(prompt, max_tokens=800, temperature=0.6)
    try:
        start = result.find('{')
        end = result.rfind('}') + 1
        if start != -1 and end > start:
            return json.loads(result[start:end])
    except:
        pass
    return {"recommended_jobs": [], "career_path": ""}'''

new6 = '''    result = call_ai(prompt, max_tokens=800, temperature=0.6)
    parsed = extract_json(result)
    if parsed:
        return parsed
    return {"recommended_jobs": [], "career_path": ""}'''

if old6 in content:
    content = content.replace(old6, new6, 1)
    changes.append("recommendations JSON ok")
else:
    changes.append("recommendations: no change needed or partial")

# Write
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("DONE:", ", ".join(changes))
