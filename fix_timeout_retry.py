import re

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# ========== 1. 把 timeout=45 改成 timeout=90 ==========
content = content.replace('timeout=45', 'timeout=90')
print('Step 1: timeout 45 -> 90: OK')

# ========== 2. 给 urlopen 加重试逻辑 ==========
# 原来的模式（timeout已经是90了）
old_block = '''    try:



        with urllib.request.urlopen(req, timeout=90) as resp:



            result = json.loads(resp.read())



            return result['choices'][0]['message']['content'].strip()



    except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:'''

new_block = '''    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                result = json.loads(resp.read())
                return result['choices'][0]['message']['content'].strip()
        except socket.timeout:
            if attempt == 0:
                continue  # 重试一次
            return '[AI生成失败: The read operation timed out]'
        except Exception as e:
            return f'[AI生成失败: {str(e)}]'

    return '[AI生成失败: Unknown error]'''

if old_block in content:
    content = content.replace(old_block, new_block)
    print('Step 2: retry logic added: OK')
else:
    print('ERROR: old_block not found, trying regex search...')
    # 用正则找
    pattern = r"(    try:\r?\n\r?\n\r?\n\r?\n        with urllib\.request\.urlopen\(req, timeout=90\) as resp:\r?\n\r?\n\r?\n\r?\n            result = json\.loads\(resp\.read\(\)\)\r?\n\r?\n\r?\n\r?\n            return result\['choices'\]\[0\]\['message'\]\['content'\]\.strip\(\)\r?\n\r?\n\r?\n\r?\n    except \(urllib\.error\.URLError, urllib\.error\.HTTPError, Exception\) as e:)"
    match = re.search(pattern, content)
    if match:
        print(f'Found at position {match.start()}-{match.end()}')
        print(repr(match.group(0)[:200]))
        content = re.sub(pattern, new_block, content)
        print('Step 2 (regex): OK')
    else:
        print('ERROR: could not find urlopen try block at all')
        print('Showing near timeout=90:')
        idx = content.find('timeout=90')
        if idx >= 0:
            print(repr(content[idx:idx+500]))

# ========== 3. 面试Q&A调用处加上 resume_text 和 supplements ==========
# 找调用 generate_interview_answers 的地方
old_interview_call = "interview_ai = generate_interview_answers(sections, target_job, matched_key, supplements)"
new_interview_call = "interview_ai = generate_interview_answers(sections, target_job, matched_key, supplements=supplements)"

if old_interview_call in content:
    content = content.replace(old_interview_call, new_interview_call)
    print('Step 3: interview call fixed: OK')
else:
    # 可能是已经修复过了？
    if 'generate_interview_answers(sections, target_job, matched_key, supplements=supplements)' in content:
        print('Step 3: interview call already fixed')
    else:
        print('ERROR: interview call not found')

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

if content != original:
    print('\nFile written successfully!')
else:
    print('\nWARNING: No changes made!')
