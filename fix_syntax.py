with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix line 417 (0-indexed 416)
lines[416] = "    return '[AI生成失败: Unknown error]'\r\n"

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Fixed line 417')
