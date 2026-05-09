# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    raw = f.read()

lines_raw = raw.split(b'\n')

print(f"Total lines: {len(lines_raw)}")

# Check lines around 5830-5845
print("\n=== Lines 5830-5845 (raw bytes) ===")
for i in range(5829, 5845):
    if i < len(lines_raw):
        line = lines_raw[i]
        tq_count = line.count(b'\x22\x22\x22')
        print(f"Line {i+1:4d}: {line[:80]} tq={tq_count}")

# Find the format_resume_as_markdown function definition
print("\n=== Searching for format_resume_as_markdown ===")
for i, line in enumerate(lines_raw):
    if b'def format_resume_as_markdown' in line:
        print(f"Found at line {i+1}")
        # Show surrounding lines
        for j in range(max(0, i-2), min(len(lines_raw), i+5)):
            print(f"  {j+1}: {lines_raw[j][:100]}")
        break

# Check: what closes the send_file call?
# Lines 5791 to end of function
print("\n=== Lines 5791-end of send_file area ===")
for i in range(5790, 5820):
    if i < len(lines_raw):
        print(f"Line {i+1:4d}: {lines_raw[i][:100]}")