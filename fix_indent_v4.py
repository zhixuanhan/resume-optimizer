"""
Strategy: Extract the logical structure of career_analysis by reading code-only lines
with their CURRENT indentation, then REBUILD with CORRECT indentation.

Step 1: Extract code lines (no blanks) with their relative indentation
Step 2: Rebuild using proper Python indentation rules
Step 3: Replace the function in the file
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

print(f"career_analysis: L{func_start+1} to L{func_end}")

# Extract code lines from the function
code_lines = []
for i in range(func_start, func_end):
    txt = get_text(lines_bytes[i])
    if txt:
        ind = get_indent(lines_bytes[i])
        code_lines.append((ind, txt))

print(f"Code lines: {len(code_lines)}")

# Now rebuild with correct indentation
# The def line's indent determines everything
def_indent = code_lines[0][0]  # indent of "def career_analysis"

# Build the output lines
output_lines = []
# Stack tracks: current expected indent level for the NEXT line
# When we see a block opener, push indent+4
# When we see dedent keywords (elif/else/except/finally), pop back

stack = [def_indent + 4]  # body of function starts at def_indent + 4

BLOCK_RE = re.compile(r'^(if|elif|else|for|while|with|try|except|finally|def|class)\b')

for i, (orig_ind, txt) in enumerate(code_lines):
    # Skip the def line itself
    if i == 0:
        output_lines.append(' ' * def_indent + txt)
        continue
    
    # Determine if this is a sibling (elif/else/except/finally)
    is_sibling = bool(re.match(r'^(elif |else:|else |except |except:|finally:)', txt))
    
    # Determine if this is a block opener
    is_opener = txt.endswith(':') and bool(BLOCK_RE.match(txt))
    
    if is_sibling:
        # Pop stack until we find the matching opener level
        # The sibling should be at the same level as the opener
        # We need to pop once (from body level back to opener level)
        while len(stack) > 1 and stack[-1] > stack[-2] + 4:
            stack.pop()
        # Pop one more to get to the opener level
        if len(stack) > 1:
            stack.pop()
        expected = stack[-1]  # same as opener
    else:
        expected = stack[-1]
    
    output_lines.append(' ' * expected + txt)
    
    if is_opener:
        stack.append(expected + 4)

# Now replace the function in the file
before = lines_bytes[:func_start]
after = lines_bytes[func_end:]

func_text = '\r\n'.join(output_lines) + '\r\n'

# Add single blank lines between logical blocks for readability
func_lines_list = func_text.split('\r\n')

result_bytes = before + [l.encode('utf-8') + b'\r\n' if not l.endswith('\r') else l.encode('utf-8') for l in func_lines_list] + list(after)

# Actually let's be more careful - join everything properly
new_raw = b''.join(
    before + 
    [line.encode('utf-8') + b'\r\n' for line in func_lines_list] +
    after
)

# Hmm, this is getting complicated. Let me just rebuild the whole file.
# Reconstruct: before part + function + after part

before_text = b'\n'.join(before).decode('utf-8', 'replace')
after_text = b'\n'.join(after).decode('utf-8', 'replace')

full_text = before_text + '\r\n' + '\r\n'.join(output_lines) + '\r\n' + after_text

with open(path, 'w', encoding='utf-8', newline='') as f:
    f.write(full_text)
print(f"Written file")

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
