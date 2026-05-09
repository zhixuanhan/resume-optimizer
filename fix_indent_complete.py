"""
Comprehensive indentation fix for career_analysis function in app.py.
Strategy: Read the whole function, track indentation stack, fix all body lines.
"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'rb') as f:
    raw = f.read()

lines = raw.split(b'\n')

def get_indent(line):
    """Count leading spaces (tabs=4)"""
    s = line.lstrip(b'\r')
    n = 0
    for b in s:
        if b == 32: n += 1
        elif b == 9: n += 4
        else: break
    return n

def get_text(line):
    return line.rstrip(b'\r\n').decode('utf-8', 'replace').strip()

# Keywords that open a new block
BLOCK_OPENERS = re.compile(r'^(if|elif|else|for|while|with|try|except|finally|def|class)\b')

# Find career_analysis function boundaries
func_start = None
func_end = None
for i, line in enumerate(lines):
    txt = get_text(line)
    if txt.startswith('def career_analysis'):
        func_start = i
    elif func_start is not None and txt.startswith('def ') and i > func_start:
        func_end = i
        break

if func_start is None:
    print("ERROR: career_analysis not found!")
    sys.exit(1)

if func_end is None:
    func_end = len(lines)

print(f"career_analysis: L{func_start+1} to L{func_end}")

# Strategy: Walk through the function, track expected indentation via a stack.
# When we see a block opener at indent N, the next non-blank line should be at N+4.
# When we see dedent (line at lower indent than expected), pop the stack.

def fix_function_indent(lines, start, end):
    """
    Fix indentation in a function body.
    Track a stack of (line_text, expected_indent) for open blocks.
    When a line's actual indent doesn't match expected, fix it.
    """
    fixed_lines = list(lines)
    changes = 0
    
    # Stack of (opener_line_idx, expected_body_indent)
    indent_stack = []
    
    # First, determine the function's base indent (the def line's indent + 4 for body)
    def_indent = get_indent(lines[start])
    body_indent = def_indent + 4
    
    # Push the function body as the initial expected indent
    indent_stack.append((start, body_indent))
    
    i = start + 1
    while i < end:
        line = fixed_lines[i]
        txt = get_text(line)
        actual_indent = get_indent(line)
        
        if not txt:  # blank line
            i += 1
            continue
        
        # Pop stack until we find a matching expected indent
        # A line can be at: expected body indent, or same as an opener (sibling), or less
        
        while len(indent_stack) > 1:
            _, expected = indent_stack[-1]
            if actual_indent >= expected:
                break
            # This line is at a lower indent than the current block expects
            # Pop back to find the right level
            indent_stack.pop()
        
        _, expected = indent_stack[-1]
        
        # Check if this line opens a new block
        is_block_opener = bool(BLOCK_OPENERS.match(txt))
        # Also check for lines ending with :
        if txt.endswith(':') and not is_block_opener:
            # Could be a one-liner or something else
            pass
        
        if is_block_opener:
            # This line should be at 'expected' indent level
            if actual_indent != expected:
                # Fix it
                content = line.rstrip(b'\r\n').lstrip(b' \t')
                fixed_lines[i] = b' ' * expected + content + b'\r\n'
                print(f"  L{i+1}: {actual_indent}sp -> {expected}sp (opener): {txt[:60]}")
                changes += 1
                actual_indent = expected
            
            # Push the body indent for next lines
            indent_stack.append((i, actual_indent + 4))
        else:
            # This is a body line - should be at 'expected' indent
            if actual_indent != expected:
                content = line.rstrip(b'\r\n').lstrip(b' \t')
                fixed_lines[i] = b' ' * expected + content + b'\r\n'
                print(f"  L{i+1}: {actual_indent}sp -> {expected}sp (body): {txt[:60]}")
                changes += 1
        
        i += 1
    
    return fixed_lines, changes

fixed_lines, changes = fix_function_indent(lines, func_start, func_end)
print(f"\nTotal changes: {changes}")

# Write and compile check
out = b'\n'.join(fixed_lines)
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
