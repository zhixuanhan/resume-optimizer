# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    raw = f.read()

lines_raw = raw.split(b'\n')

# Check lines 5790-5840 for triple quotes
print("=== Triple quote analysis (lines 5790-5845) ===")
for i in range(5789, 5845):
    if i < len(lines_raw):
        line = lines_raw[i]
        tq_positions = []
        for j in range(len(line) - 2):
            if line[j:j+3] == b'\x22\x22\x22':
                tq_positions.append(j)
        tq_count = len(tq_positions)
        marker = " <<< LINE 5839" if i == 5838 else ""
        if tq_count > 0:
            print(f"Line {i+1:4d}: {line[:80]} tq_pos={tq_positions}{marker}")
        else:
            if i in [5837, 5838, 5839, 5840]:
                print(f"Line {i+1:4d}: {line[:80]} (no tq){marker}")

# Look for unclosed string before line 5839
print("\n=== Looking for unclosed string before line 5839 ===")
# Search backwards from line 5839 for the start of multi-line string
for i in range(5838, 5750, -1):
    line = lines_raw[i]
    if b'\x22\x22\x22' in line:
        print(f"Line {i+1} has triple quote: {line[:60]}")
        # Check: is it opening or closing?
        # Count triple quotes in this line
        tq = b'\x22\x22\x22'
        positions = []
        for j in range(len(line)-2):
            if line[j:j+3] == tq:
                positions.append(j)
        print(f"  Triple quotes at byte positions: {positions}")
        # Check if line ends with \r
        if line and line[-1] == 13:
            print(f"  Ends with CR (\\r)")
        # Check if line is odd/even count
        if len(positions) % 2 != 0:
            print(f"  ODD count ({len(positions)}) - this could be the start!")
        break