import re

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# 精确定位 urlopen try 块
old = (
    '    try:\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '        with urllib.request.urlopen(req, timeout=90) as resp:\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '            result = json.loads(resp.read())\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '            return result[\'choices\'][0][\'message\'][\'content\'].strip()\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '    except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:'
)

new = (
    '    for attempt in range(2):\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '        try:\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '            with urllib.request.urlopen(req, timeout=90) as resp:\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '                result = json.loads(resp.read())\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '                return result[\'choices\'][0][\'message\'][\'content\'].strip()\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '        except socket.timeout:\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '            if attempt == 0:\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '                continue  # 重试一次\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '            return \'[AI生成失败: The read operation timed out]\'\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '        except Exception as e:\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '            return f\'[AI生成失败: {str(e)}]\'\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
    '    return \'[AI生成失败: Unknown error]\'\r\n\r\n\r\n\r\n\r\n\r\n\r\n'
)

if old in content:
    content = content.replace(old, new)
    print('SUCCESS: retry logic added!')
else:
    print('ERROR: exact pattern not found')
    # 显示实际内容
    idx = content.find('with urllib.request.urlopen(req, timeout=90)')
    if idx >= 0:
        print('Actual content:')
        print(repr(content[idx-200:idx+600]))

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

if content != original:
    print('File written.')
else:
    print('No changes made!')
