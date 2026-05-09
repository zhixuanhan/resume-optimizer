"""
v5 FINAL: Rebuild career_analysis with correct indentation.
Based on the structure dump, we know exactly what's wrong.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'rb') as f:
    raw = f.read()

lines_bytes = raw.split(b'\n')

def get_indent(line):
    s = line.lstrip(b'\r')
    n = 0
    for b in s:
        if b == 32: n += 1
        elif b == 9: n += 4
        else: break
    return n

def get_text(line):
    return line.rstrip(b'\r\n').decode('utf-8', 'replace').strip()

# Find career_analysis
func_start = None
func_end = None
for i, line in enumerate(lines_bytes):
    txt = get_text(line)
    if txt.startswith('def career_analysis'):
        func_start = i
    elif func_start is not None and txt.startswith('def ') and i > func_start:
        func_end = i
        break
if func_end is None:
    func_end = len(lines_bytes)

# Extract code lines
code_lines = []
for i in range(func_start, func_end):
    txt = get_text(lines_bytes[i])
    if txt:
        ind = get_indent(lines_bytes[i])
        code_lines.append((ind, txt))

# The correct structure should be:
# 0sp: def career_analysis():
# 4sp:   try:
# 8sp:     data = request.json              (try body)
# 8sp:     ...
# 8sp:     if not os.path.exists(...):       (try body)
# 12sp:      return jsonify(...)             (if body)
# 8sp:     with open(...) as f:              (try body - sibling of if)
# 12sp:      session_data = json.load(f)     (with body)
# 12sp:      sections = ...                  (with body)
# 12sp:      matched_key, career_info = ...  (with body)
# 12sp:      if not career_info:             (with body)
# 16sp:        return jsonify(...)           (if body)
# 12sp:      # AI analysis                   (with body)
# 12sp:      comp_str = ...                  (with body)
# ...
# 12sp:      if match_score >= 70:           (with body)
# 16sp:        match_level = ...             (if body)
# 16sp:        base_advice = ...             (if body)
# 12sp:      elif match_score >= 40:         (with body)
# 16sp:        match_level = ...             (elif body)
# 16sp:        base_advice = ...             (elif body)
# 12sp:      else:                           (with body)
# 16sp:        match_level = ...             (else body)
# 16sp:        base_advice = ...             (else body)
# 12sp:      response = {                    (with body)
# 12sp:          "job_name": ...             (dict value)
# ...
# 12sp:      }                               (with body)
# 12sp:      session_data['career_info'] =   (with body)
# 12sp:      session_data['target_job'] =    (with body)
# 12sp:      with open(...) as f:            (with body)
# 16sp:        json.dump(...)                (with body)
# 16sp:        return jsonify(response)      (with body)
# 4sp:   except Exception as e:              (sibling of try)
# 8sp:     import traceback                  (except body)
# 8sp:     traceback.print_exc()             (except body)
# 8sp:     return jsonify(...)               (except body)

# The mapping from current structure to correct:
# Code line index -> correct indent
indent_map = [
    # idx, correct_indent, description
    (0, 0),    # def career_analysis():
    (1, 4),    # try:
    (2, 8),    # data = request.json
    (3, 8),    # session_id = ...
    (4, 8),    # target_job = ...
    (5, 8),    # session_file = ...
    (6, 8),    # if not os.path.exists
    (7, 12),   # return jsonify({"error": ...}) -- if body
    (8, 8),    # with open(session_file, 'r', ...) as f: -- try body, not if body!
    (9, 12),   # session_data = json.load(f) -- with body
    (10, 12),  # sections = ... -- with body
    (11, 12),  # all_text = ... -- with body
    (12, 12),  # matched_key, career_info = ... -- with body
    (13, 12),  # if not career_info: -- with body
    (14, 16),  # return jsonify({ -- if body
    (15, 16),  # "error": ... -- dict value (inside return)
    (16, 16),  # "available_jobs": ... -- dict value
    (17, 16),  # }), 404 -- closing return
    (18, 12),  # # 用 AI 做个性化职业分析 -- with body
    (19, 12),  # comp_str = ... -- with body
    (20, 12),  # ai_prompt = f"... -- with body
    (21, 12),  # ai_result = call_ai(...) -- with body
    (22, 12),  # ai_data = extract_json(...) -- with body
    (23, 12),  # # 关键词匹配 -- with body
    (24, 12),  # job_kws = ... -- with body
    (25, 12),  # matched_kws = ... -- with body
    (26, 12),  # missing_kws = ... -- with body
    (27, 12),  # has_internship = ... -- with body
    (28, 12),  # has_project = ... -- with body
    (29, 12),  # match_score = ... -- with body
    (30, 12),  # match_score = max(...) -- with body
    (31, 12),  # if match_score >= 70: -- with body
    (32, 16),  # match_level = "🟢" -- if body
    (33, 16),  # base_advice = ... -- if body
    (34, 12),  # elif match_score >= 40: -- sibling of if
    (35, 16),  # match_level = "🟡" -- elif body
    (36, 16),  # base_advice = ... -- elif body
    (37, 12),  # else: -- sibling of elif
    (38, 16),  # match_level = "🔴" -- else body
    (39, 16),  # base_advice = ... -- else body
    (40, 12),  # response = { -- with body (AFTER if/elif/else)
    (41, 16),  # "job_name": ... -- dict value
    (42, 16),  # "job_aliases": ... -- dict value
    (43, 16),  # "match_score": ... -- dict value
    (44, 16),  # "match_level": ... -- dict value
    (45, 16),  # "match_advice": ... -- dict value
    (46, 16),  # "matched_keywords": ... -- dict value
    (47, 16),  # "missing_keywords": ... -- dict value
    (48, 16),  # "transferable_skills": ... -- dict value
    (49, 16),  # "career_advice": ... -- dict value
    (50, 16),  # "has_internship": ... -- dict value
    (51, 16),  # "has_project": ... -- dict value
    (52, 16),  # "salary": ... -- dict value
    (53, 16),  # "market": ... -- dict value
    (54, 16),  # "daily_work": ... -- dict value
    (55, 16),  # "dev_path": ... -- dict value
    (56, 16),  # "competencies": ... -- dict value
    (57, 16),  # "interview_qa": ... -- dict value
    (58, 16),  # } -- dict close
    (59, 12),  # session_data['career_info'] = response -- with body
    (60, 12),  # session_data['target_job'] = target_job -- with body
    (61, 12),  # with open(session_file, 'w', ...) as f: -- with body
    (62, 16),  # json.dump(...) -- nested with body
    (63, 16),  # return jsonify(response) -- nested with body
    (64, 4),   # except Exception as e: -- sibling of try
    (65, 8),   # import traceback -- except body
    (66, 8),   # traceback.print_exc() -- except body
    (67, 8),   # return jsonify(...) -- except body
]

if len(indent_map) != len(code_lines):
    print(f"WARNING: indent_map has {len(indent_map)} entries but code has {len(code_lines)} lines!")
    print("Falling back to auto-detection...")
    sys.exit(1)

# Build output lines with correct indentation
output = []
for i, (correct_ind, txt) in enumerate(zip([m[1] for m in indent_map], [c[1] for c in code_lines])):
    output.append(' ' * correct_ind + txt)

# Reconstruct file
before = b'\n'.join(lines_bytes[:func_start])
after = b'\n'.join(lines_bytes[func_end:])

func_text = '\r\n'.join(output)

full = before.decode('utf-8', 'replace') + '\r\n' + func_text + '\r\n' + after.decode('utf-8', 'replace')

with open(path, 'w', encoding='utf-8', newline='') as f:
    f.write(full)

print(f"Written {len(full)} bytes")

try:
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    compile(src, path, 'exec')
    print("COMPILE OK! ✅")
except SyntaxError as e:
    print(f"SyntaxError L{e.lineno}: {e.msg}")
    ls = src.split('\n')
    for j in range(max(0, e.lineno-5), min(len(ls), e.lineno+4)):
        m = '>>> ' if j == e.lineno-1 else '    '
        print(f'{m}{j+1}: {repr(ls[j][:120])}')
