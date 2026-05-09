# -*- coding: utf-8 -*-
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'

# Read as bytes, detect encoding
with open(path, 'rb') as f:
    raw = f.read()

# Detect if it's utf-8 or gbk
try:
    text = raw.decode('utf-8')
    encoding = 'utf-8'
except UnicodeDecodeError:
    text = raw.decode('gbk', errors='replace')
    encoding = 'gbk'

print(f"Detected encoding: {encoding}, len={len(text)}")

changes = []

# ===== 1. Add pdfplumber import after PyPDF2 import =====
if 'HAS_PDFPLUMBER' not in text:
    # Find the PyPDF2 import line
    m = re.search(r"(from PyPDF2 import PdfReader\r?\n\r?\n)(# =====|# ===|def call_ai)", text)
    if m:
        insertion = m.group(1) + """# pdfplumber - better PDF parsing (install with: pip install pdfplumber)
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

"""
        text = text[:m.start(2)] + insertion + text[m.start(2):]
        changes.append("pdfplumber import added")
    else:
        changes.append("pdfplumber: pattern not found, trying alt")
        # alt: after PyPDF2 import
        idx = text.find('from PyPDF2 import PdfReader')
        if idx >= 0:
            end = text.find('\n', idx) + 1
            ins = text[:end] + """
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False
"""
            # find next meaningful line
            next_line = text.find('\n', end)
            rest = text[next_line:]
            text = ins + rest
            changes.append("pdfplumber import added (alt)")

# ===== 2. Replace extract_text_from_pdf with dual-method version =====
old_func = re.search(r"def extract_text_from_pdf\(pdf_path\):.*?(?=\ndef |\nclass |\Z)", text, re.DOTALL)
if old_func:
    new_func = """def extract_text_from_pdf(pdf_path):
    \"\"\"Dual PDF parsing to maximize text extraction\"\"\"
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
    
    # Method 2: pdfplumber (better at tables and layout)
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
        return "[PDF parse failed - please check the file]"
    
    combined = "\\n".join(texts)
    # Remove control characters
    combined = re.sub(r"[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f\\x7f-\\x9f]", "", combined)
    return combined.strip()

"""
    text = text.replace(old_func.group(0), new_func, 1)
    changes.append("extract_text_from_pdf replaced")
else:
    changes.append("extract_text_from_pdf: not found")

# ===== 3. Fix career API JSON parsing =====
if 'extract_json(ai_result)' not in text:
    # Find the pattern
    m = re.search(r"(ai_result = call_ai\(ai_prompt, max_tokens=600.*?\))\r?\n(\s+)(try:\s+start = ai_result\.find\('\{'\).*?)(ai_data = \{\})", 
                  text, re.DOTALL)
    if m:
        replacement = m.group(1) + "\n" + m.group(2) + "ai_data = extract_json(ai_result) or {}"
        text = text.replace(m.group(0), replacement, 1)
        changes.append("career API JSON fixed")
    else:
        # Try simpler pattern
        idx = text.find("try:\n        start = ai_result.find('{')")
        if idx >= 0:
            end = text.find("ai_data = {}", idx)
            if end > idx:
                text = text[:idx] + "ai_data = extract_json(ai_result) or {}\n" + text[end + len("ai_data = {}"):]
                changes.append("career API JSON fixed (simple)")
        else:
            changes.append("career API: pattern not found")

# ===== 4. Fix recommendations JSON parsing =====
if text.count('extract_json(result)') < 2:
    # There's already one for _get_ai_job_recommendations
    # But we need the one for the career API too
    m = re.search(r"(result = call_ai\(prompt, max_tokens=800, temperature=0\.6\))\r?\n(\s+)(try:\s+start = result\.find\('\{'\).*?)(return \{\"recommended_jobs\": \[\], \"career_path\": \"\"\}\})",
                  text, re.DOTALL)
    if m:
        replacement = m.group(1) + "\n" + m.group(2) + "parsed = extract_json(result)\n" + m.group(2) + "if parsed:\n" + m.group(2) + "    return parsed\n" + m.group(2) + "return {\"recommended_jobs\": [], \"career_path\": \"\"}"
        text = text.replace(m.group(0), replacement, 1)
        changes.append("recommendations JSON fixed")
    else:
        changes.append("recommendations: pattern not found")

# Write back
with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

print("Changes made:", ", ".join(changes))

# Verify
with open(path, 'r', encoding='utf-8') as f:
    verify = f.read()
checks = [
    ('extract_json exists', 'def extract_json' in verify),
    ('pdfplumber HAS_PDFPLUMBER', 'HAS_PDFPLUMBER' in verify),
    ('dual extract_text', 'pdfplumber.open' in verify),
    ('diagnose uses extract_json', 'parsed = extract_json(result)' in verify),
    ('career uses extract_json', 'extract_json(ai_result)' in verify),
    ('recommend uses extract_json', 'parsed = extract_json(result)' in verify),
]
for name, ok in checks:
    print(('OK' if ok else 'MISS'), name)
