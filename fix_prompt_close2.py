# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# The prompt content ends at line 4315 (0-indexed 4314)
# That's: '请直接输出6个Q&A：\n'
print("Line 4315:", repr(lines[4314]))

# The f-string opened at line 4291 with f"""
# Now close it right after line 4315
# Insert """ between line 4315 and the blank lines that follow

new_lines = [
    '    """',  # close the f-string
    '\n'
]

# Build new file: lines up to and including line 4315, then """, then rest
# Actually, line 4315 ends with '请直接输出6个Q&A：\n'
# After that comes blank lines (4316-4322), then 'result = call_ai' (4323)
# We need to insert """ after line 4315 (index 4314)
result_lines = lines[:4315]  # lines 0 to 4314 (line 1 to 4315)
result_lines.append('    """\n')  # close the f-string
result_lines.extend(lines[4315:])  # rest of file

with open(app_path, 'w', encoding='utf-8') as f:
    f.writelines(result_lines)

# Verify
import ast
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()
try:
    ast.parse(content)
    print("SYNTAX OK! File is valid Python.")
    print(f"New file: {len(result_lines)} lines")
except SyntaxError as e:
    print(f"Still broken: {e.msg} at line {e.lineno}")
    ctx = content.split('\n')
    for i in range(max(0, e.lineno-3), min(len(ctx), e.lineno+2)):
        marker = ">>> " if i == e.lineno-1 else "    "
        print(f"  {i+1}: {marker}{repr(ctx[i][:80])}")