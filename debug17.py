# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Line 4327 (0-indexed = 4326) is: '    return result\n'
# We need to insert """ right after it (as a new line before the blank lines)
# But let me first verify this is the right place
print("Line 4326 (return result):", repr(lines[4326]))
print("Line 4327:", repr(lines[4327]))
print("Line 4328:", repr(lines[4328]))

# Check: line 4323 should be call_ai
print("Line 4323:", repr(lines[4322]))

# The fix: insert """ before the blank line that precedes result = call_ai
# Actually the closing """ should be right before '    result = call_ai'
# Let me check line 4322 (call_ai) and 4323 (blank before it)
print("\nLines 4319-4330:")
for i in range(4318, 4330):
    print(f"  {i+1}: {repr(lines[i][:60])}")

# The opening f""" is on line 4291, after the prompt content ends at line 4315 (请直接输出6个Q&A：)
# The natural place to close is right before '    result = call_ai'
# which is line 4323 (0-indexed = 4322)
# But wait - let me check if there's a closing """ somewhere between 4315 and 4322
print("\nSearching for closing triple quote between 4315-4325...")
for i in range(4314, 4325):
    if '"""' in lines[i]:
        print(f"  Found at line {i+1}: {repr(lines[i])}")