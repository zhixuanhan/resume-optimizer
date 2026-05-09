# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    raw = f.read()

lines_raw = raw.split(b'\n')

# Check 5790-5760 backwards for triple quotes (searching for unclosed string start)
print("=== Scanning for unclosed multi-line string (searching backwards from 5790) ===")
for i in range(5789, 5700, -1):
    line = lines_raw[i]
    tq_positions = []
    for j in range(len(line) - 2):
        if line[j:j+3] == b'\x22\x22\x22':
            tq_positions.append(j)
    tq_count = len(tq_positions)
    marker = f"line {i+1}" 
    if tq_count > 0:
        print(f"  {marker}: tq_count={tq_count}, positions={tq_positions}, content={line[:80]}")
    # Also show lines that might be inside a string
    if i in [5790, 5788, 5785, 5780, 5775]:
        print(f"  {marker} (context): {line[:80] if line else '<EMPTY>'}")

# Now check what tokenize thinks is the issue
print("\n=== Tokenizer analysis ===")
import tokenize
import io
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

lines_text = content.split('\n')
tokens = list(tokenize.generate_tokens(io.StringIO(content).readline))
for tok in tokens:
    if tok.type == tokenize.STRING:
        if '"""' in tok.string or "'''" in tok.string:
            print(f"STRING at line {tok.start[0]}: {repr(tok.string[:60])}")
    if tok.type == tokenize.ERRORTOKEN:
        print(f"ERROR at line {tok.start[0]}: {repr(tok.string)}")

print("\n=== Around line 5839 (the reported error line) ===")
for i in range(5836, 5843):
    if i < len(lines_text):
        print(f"  {i+1}: {repr(lines_text[i][:80])}")