"""
Fix indentation in career_analysis by analyzing the ACTUAL block structure.
Strategy: 
1. Strip blank lines to get code-only view
2. Track block openers and their expected body indent
3. Fix body lines that don't match expected indent
"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'rb') as f:
    raw = f.read()

lines = raw.split(b'\n')

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
for i, line in enumerate(lines):
    txt = get_text(line)
    if txt.startswith('def career_analysis'):
        func_start = i
    elif func_start is not None and txt.startswith('def ') and i > func_start:
        func_end = i
        break
if func_end is None:
    func_end = len(lines)

print(f"career_analysis: L{func_start+1} to L{func_end}")

# Collect only non-blank code lines with their real indices
code_lines = []  # (real_index, indent, text)
for i in range(func_start, func_end):
    txt = get_text(lines[i])
    if txt:
        ind = get_indent(lines[i])
        code_lines.append((i, ind, txt))

# Build a stack-based indent tracker
# Key insight: When a block opener (if/elif/else/for/with/try/except) is at indent N,
# the NEXT code line should be at N+4. If it's at N or less, it's a sibling, not a body.
# When we see a dedent, we pop back to that level.

# First, let's figure out what the CORRECT indent should be for each code line
# by tracking block openers and their children.

BLOCK_OPENERS = re.compile(r'^(if|elif|else|for|while|with|try|except|finally|def|class)\b')

correct_indent = {}  # real_index -> expected indent

# Stack: [(opener_real_idx, opener_indent, body_indent)]
stack = []

# def career_analysis is at indent 4sp (or 0sp if top-level)
def_indent = get_indent(lines[func_start])
# The first line of function body should be at def_indent + 4
stack.append((func_start, def_indent, def_indent + 4))

changes = 0
for real_idx, actual_indent, txt in code_lines[1:]:  # skip def line itself
    # Pop stack until body_indent <= actual_indent
    while len(stack) > 1:
        _, opener_ind, body_ind = stack[-1]
        if actual_indent >= body_ind:
            break
        stack.pop()
    
    _, opener_ind, body_ind = stack[-1]
    expected = body_ind
    
    # Is this a block opener?
    is_opener = bool(BLOCK_OPENERS.match(txt)) or txt.endswith(':')
    
    # Check if this line is a dedent (sibling of something on the stack)
    # e.g., elif/else should be at the same indent as if, not at body_ind
    if txt.startswith(('elif ', 'else:', 'except ', 'except:', 'finally:')):
        # These are siblings of the last opener
        # Pop until we find the matching opener
        while len(stack) > 1:
            _, oi, bi = stack[-1]
            if actual_indent == oi:
                break
            stack.pop()
        _, opener_ind, _ = stack[-1]
        expected = opener_ind  # same as the opener
        is_opener = True
    
    # Record expected indent
    correct_indent[real_idx] = expected
    
    # If this opens a new block, push to stack
    if is_opener and txt.endswith(':'):
        stack.append((real_idx, expected, expected + 4))

# Now fix lines that have wrong indent
for real_idx, expected in correct_indent.items():
    actual = get_indent(lines[real_idx])
    if actual != expected:
        content = lines[real_idx].rstrip(b'\r\n').lstrip(b' \t')
        lines[real_idx] = b' ' * expected + content + b'\r\n'
        txt = get_text(lines[real_idx])
        print(f"  L{real_idx+1}: {actual}sp -> {expected}sp: {txt[:60]}")
        changes += 1

print(f"\nTotal changes: {changes}")

out = b'\n'.join(lines)
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
