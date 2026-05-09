"""
v5: Extract code lines, print current structure, then rebuild with correct indent.
Key: track the ACTUAL block structure from the keywords, not from the broken indents.
"""
import sys, re
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

# Print the structure
print("=== Current structure (code lines only) ===")
for i, (ind, txt) in enumerate(code_lines):
    level = ind // 4
    prefix = "  " * level
    print(f"{i:3d} [{ind:2d}sp] {prefix}{txt[:80]}")

print(f"\nTotal: {len(code_lines)} code lines")
