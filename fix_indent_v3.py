"""
Complete fix: Remove excess blank lines from career_analysis, then rebuild indentation
using Python's own tokenizer to understand block structure.
"""
import sys, re, token, tokenize, io
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

# === STEP 1: Remove excess blank lines in career_analysis ===
# Find function boundaries
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

# Before function - keep as-is
# Function area - strip excess blank lines (max 1 blank line between code lines)
before = lines_bytes[:func_start]
after = lines_bytes[func_end:]

func_lines = lines_bytes[func_start:func_end]
cleaned = []
prev_blank = False
for line in func_lines:
    txt = get_text(line)
    if not txt:
        if not prev_blank:
            cleaned.append(b'\r\n')  # single blank line
            prev_blank = True
    else:
        # Keep the line with its content, normalize to \r\n
        content = line.rstrip(b'\r\n').lstrip()  # strip indent + line ending
        # We'll re-add indent later, for now just keep content
        cleaned.append(line.rstrip(b'\r\n') + b'\r\n')
        prev_blank = False

# Now we have clean function lines (no excess blanks)
# Rejoin and try to figure out the correct structure

# === STEP 2: Extract just the code (no blanks), track structure ===
code_items = []  # (index_in_cleaned, indent, text)
for i, line in enumerate(cleaned):
    txt = get_text(line)
    if txt:
        ind = get_indent(line)
        code_items.append((i, ind, txt))

print(f"Code lines in function: {len(code_items)}")

# === STEP 3: Determine correct indentation for each code line ===
# Use a stack-based approach. The key rules:
# 1. After a block opener (ending with :), next line indent += 4
# 2. elif/else/except/finally at same indent as matching if/try
# 3. Dedent: when indent decreases, pop stack

BLOCK_RE = re.compile(r'^(if|elif|else|for|while|with|try|except|finally|def|class)\b')

# We need to determine the INTENDED indent based on the STRUCTURE, not the current broken indent.
# Strategy: use the CURRENT indents as hints, but fix obvious errors.
# 
# The function def is at some indent (e.g., 4sp for a route).
# Inside the function body, code is at def_indent + 4.
# A try: inside the function is at def_indent + 4.
# Code inside try is at def_indent + 8.
# etc.

def_indent = get_indent(lines_bytes[func_start])

# Build stack: [(indent_level, is_block_opener)]
# Process code items in order
stack = [def_indent]  # stack of expected indent levels
correct = {}  # index_in_cleaned -> correct indent

for idx, actual_ind, txt in code_items:
    # Pop stack until we find a level <= actual_ind
    while len(stack) > 1 and stack[-1] > actual_ind:
        stack.pop()
    
    # Is this a sibling (elif/else/except/finally)?
    is_sibling = txt.startswith(('elif ', 'else:', 'else :', 'except ', 'except:', 'finally:'))
    
    if is_sibling:
        # Should be at the same level as the last block opener
        # Pop one more to get the opener's level
        if len(stack) > 1:
            stack.pop()
        expected = stack[-1]  # same as opener
    else:
        expected = stack[-1]
    
    correct[idx] = expected
    
    # If this opens a new block, push new level
    if txt.endswith(':') and (BLOCK_RE.match(txt) or txt.endswith(':')):
        stack.append(expected + 4)

# === STEP 4: Apply corrections ===
changes = 0
for idx, expected in correct.items():
    line = cleaned[idx]
    actual = get_indent(line)
    if actual != expected:
        content = line.rstrip(b'\r\n').lstrip(b' \t')
        cleaned[idx] = b' ' * expected + content + b'\r\n'
        txt = content.decode('utf-8', 'replace')[:60]
        print(f"  L{idx+1}: {actual}sp -> {expected}sp: {txt}")
        changes += 1

print(f"\nIndent changes: {changes}")

# === STEP 5: Reassemble the file ===
result = before + cleaned + after
out = b'\n'.join(result)
if not out.endswith(b'\n'):
    out += b'\n'

with open(path, 'wb') as f:
    f.write(out)
print(f"Written {len(out)} bytes")

try:
    compile(out.decode('utf-8'), path, 'exec')
    print("COMPILE OK! ✅")
except SyntaxError as e:
    print(f"SyntaxError L{e.lineno}: {e.msg}")
    src = out.decode('utf-8').split('\n')
    for j in range(max(0, e.lineno-5), min(len(src), e.lineno+4)):
        m = '>>> ' if j == e.lineno-1 else '    '
        print(f'{m}{j+1}: {repr(src[j][:120])}')
