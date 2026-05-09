with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = (
    "    try:\n\n\n\n\n\n\n\n        with urllib.request.urlopen(req, timeout=90) as resp:\n\n\n\n\n\n\n\n            result = json.loads(resp.read())\n\n\n\n\n\n\n\n            return result['choices'][0]['message']['content'].strip()\n\n\n\n\n\n\n\n"
)

new_block = (
    "    for attempt in range(2):\n\n\n\n\n\n\n\n        try:\n\n\n\n\n\n\n\n            with urllib.request.urlopen(req, timeout=90) as resp:\n\n\n\n\n\n\n\n                result = json.loads(resp.read())\n\n\n\n\n\n\n\n                return result['choices'][0]['message']['content'].strip()\n\n\n\n\n\n\n\n        except socket.timeout:\n\n\n\n\n\n\n\n            if attempt == 0:\n\n\n\n\n\n\n\n                continue  # 重试一次\n\n\n\n\n\n\n\n            return '[AI生成失败: The read operation timed out]'\n\n\n\n\n\n\n\n        except Exception as e:\n\n\n\n\n\n\n\n            return f'[AI生成失败: {str(e)}]'\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    return '[AI生成失败: Unknown error]\n\n\n\n\n\n\n\n"
)

if old_block in content:
    content = content.replace(old_block, new_block)
    print('SUCCESS: retry logic added!')
else:
    print('ERROR: exact pattern not found')
    import sys
    sys.exit(1)

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('File written.')
