# -*- coding: utf-8 -*-
import tokenize
import io

app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File: {len(content)} chars")

# Use tokenizer to find issues
print("\n--- Token analysis ---")
tokens = []
try:
    tokenizer = tokenize.generate_tokens(io.StringIO(content).readline)
    for i, tok in enumerate(tokenizer):
        tokens.append(tok)
        if tok.type == tokenize.ERRORTOKEN:
            print(f"ERROR TOKEN at line {tok.start[0]}: {repr(tok.string)}")
except tokenize.TokenError as e:
    print(f"TokenError: {e}")
except Exception as e:
    print(f"Exception: {e}")

# Check for unclosed strings
print("\n--- String literal analysis ---")
import ast
try:
    ast.parse(content)
    print("AST: OK")
except SyntaxError as e:
    print(f"AST SyntaxError at line {e.lineno}: {e.msg}")
    lines = content.split('\n')
    # Show context
    start = max(0, e.lineno - 3)
    end = min(len(lines), e.lineno + 2)
    for i in range(start, end):
        marker = ">>> " if i == e.lineno - 1 else "    "
        print(f"{i+1}: {marker}{repr(lines[i][:100])}")
