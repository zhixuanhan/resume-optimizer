# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Check line 4315 - it contains "请直接输出6个Q&A："
print("Line 4316:", repr(lines[4315]))
print("Line 4317:", repr(lines[4316]))
print("Line 4323:", repr(lines[4322]))  # call_ai

# The closing """ should go after line 4316 (the prompt content ends)
# and before line 4317 (blank line), so that the f-string closes
# before the Python code 'result = call_ai'

# Current structure:
# Line 4316: ...请直接输出6个Q&A：\n
# Line 4317-4322: blank lines
# Line 4323:     result = call_ai(...)

# The fix: add """ after line 4316 (index 4315)
# This closes the f-string, then the blank lines and call_ai are normal Python

old_line = lines[4315]  # Should be: '请直接输出6个Q&A：\n'
new_lines = [old_line, '"""', '\n']

print("\nCurrent line 4316:", repr(old_line))
print("Next line:", repr(lines[4316]))

# Check: line 4315 contains the closing part?
if '请直接输出6个Q&A' in old_line:
    print("Found prompt ending at line 4316!")
    # Insert """ right after this line
    lines_after = lines[4316:]
    lines = lines[:4316] + ['"""', '\n'] + lines_after
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    # Verify
    import ast
    with open(app_path, 'r', encoding='utf-8') as f:
        content = f.read()
    try:
        ast.parse(content)
        print("SYNTAX OK! File is now valid Python.")
    except SyntaxError as e:
        print(f"Still broken: {e.msg} at line {e.lineno}")
        # Show context
        ctx_lines = content.split('\n')
        for i in range(max(0, e.lineno-3), min(len(ctx_lines), e.lineno+2)):
            marker = ">>> " if i == e.lineno-1 else "    "
            print(f"  {i+1}: {marker}{repr(ctx_lines[i][:80])}")
else:
    print("Line 4316 doesn't have expected content. Searching...")
    for i in range(4314, 4325):
        print(f"  {i+1}: {repr(lines[i][:60])}")