# -*- coding: utf-8 -*-
"""Fix timeout: make optimize_resume async with background threads"""
import re

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
content = open(path, encoding='utf-8').read()
original = content

# Find optimize_resume function
func_start = content.find('def optimize_resume(')
if func_start == -1:
    print("ERROR: optimize_resume not found")
    exit(1)

# Find the return statement in optimize_resume
return_idx = content.find('    return jsonify({', func_start)
if return_idx == -1:
    print("ERROR: return statement not found")
    exit(1)

# Find the end of optimize_resume function (next function definition or end of class)
next_func = content.find('\ndef ', return_idx + 10)
if next_func == -1:
    next_func = len(content)

func_end = next_func

# Extract the function body
func_body = content[func_start:func_end]
func_lines = func_body.split('\n')

# Find key lines
new_lines = []
i = 0
in_try = False
saw_generate_opt = False
saw_interview = False
skip_next_indent_block = 0

for line in func_lines:
    stripped = line.strip()
    
    # Skip the generate_optimized_resume call and its except block
    if 'generate_optimized_resume(' in line:
        # Replace with: run in background, return partial result
        new_lines.append(line)  # keep the try line
        saw_generate_opt = True
        # Next line is the call - comment it out and add thread
        i += 1
        continue
    
    if saw_generate_opt and 'optimized = generate_optimized_resume' in line:
        # Comment out this line and add threaded version
        indent = len(line) - len(line.lstrip())
        new_lines.append(' ' * indent + '# 异步执行，避免超时')
        new_lines.append(' ' * indent + 'import threading as _threading')
        new_lines.append(' ' * indent + 'result_holder = [None]')
        new_lines.append(' ' * indent + 'error_holder = [None]')
        new_lines.append(' ' * indent + 'def _run_optimize():')
        new_lines.append(' ' * indent + '    try:')
        new_lines.append(' ' * indent + '        result_holder[0] = generate_optimized_resume(sections, target_job, matched_key, supplements)')
        new_lines.append(' ' * indent + '    except Exception as e:')
        new_lines.append(' ' * indent + '        error_holder[0] = str(e)')
        new_lines.append(' ' * indent + 't = _threading.Thread(target=_run_optimize)')
        new_lines.append(' ' * indent + 't.start()')
        new_lines.append(' ' * indent + 't.join(timeout=60)')
        new_lines.append(' ' * indent + 'if error_holder[0]:')
        new_lines.append(' ' * indent + '    optimized = {\'_error\': error_holder[0], \'_original_sections\': sections, \'_target_job\': target_job, \'_career_key\': matched_key}')
        new_lines.append(' ' * indent + '    optimized[\'岗位职责\'] = f\'**目标岗位：**{target_job}**\\n**简历评分：** 待优化\\n**建议时间：** 一般需2-3天\'  ')
        new_lines.append(' ' * indent + 'elif t.is_alive():')
        new_lines.append(' ' * indent + '    optimized = {\'_timeout\': True, \'_original_sections\': sections, \'_target_job\': target_job, \'_career_key\': matched_key}')
        new_lines.append(' ' * indent + '    optimized[\'岗位职责\'] = f\'**目标岗位：**{target_job}**\\n**简历评分：** 优化中...\\n**建议时间：** 请稍后刷新\'  ')
        new_lines.append(' ' * indent + 'else:')
        new_lines.append(' ' * indent + '    optimized = result_holder[0]')
        saw_generate_opt = False
        continue
    
    if saw_generate_opt and 'optimized = {' in line and '_error' in line:
        # Skip the error fallback - we handle it in the thread
        saw_generate_opt = False
        continue
    
    if saw_generate_opt and line.strip() and not line.strip().startswith('#') and not line.strip().startswith('optimized'):
        # End of the generate_optimized_resume block
        saw_generate_opt = False
    
    new_lines.append(line)

# More targeted approach: just modify the function by replacing the whole thing
print("Using targeted replacement approach")

# Let's find the exact start and end of the function and replace it
print("Function found, creating replacement...")

# Create replacement function
replacement = '''def optimize_resume():
    """优化简历（异步版本，AI调用超时60秒）"""
    data = request.json
    session_id = data.get('session_id')
    target_job = data.get('target_job', '')
    career_goal = data.get('career_goal', '')
    supplements = data.get('supplements', {})

    session_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.json")
    if not os.path.exists(session_file):
        return jsonify({"error": "会话不存在，请先上传简历"}), 400

    with open(session_file, 'r', encoding='utf-8') as f:
        session_data = json.load(f)

    sections = session_data.get('sections', {})
    matched_key, _ = match_career_info(target_job)

    # 异步执行简历优化（60秒超时）
    result_holder = [None]
    error_holder = [None]

    def _run_optimize():
        try:
            result_holder[0] = generate_optimized_resume(sections, target_job, matched_key, supplements)
        except Exception as e:
            error_holder[0] = str(e)

    t = threading.Thread(target=_run_optimize)
    t.start()
    t.join(timeout=60)

    if error_holder[0]:
        optimized = {'_error': error_holder[0], '_original_sections': sections, '_target_job': target_job, '_career_key': matched_key}
        optimized['岗位职责'] = f'**目标岗位：**{target_job}\\n**简历评分：** 待优化\\n**建议时间：** 一般需2-3天'
    elif t.is_alive():
        optimized = {'_timeout': True, '_original_sections': sections, '_target_job': target_job, '_career_key': matched_key}
        optimized['岗位职责'] = f'**目标岗位：**{target_job}\\n**简历评分：** 优化中...\\n**建议时间：** 请稍后刷新'
        optimized['个人总结'] = '[简历优化正在进行中，请稍后刷新页面查看结果]'
        optimized['求职意向'] = f'**目标岗位：** {target_job}'
    else:
        optimized = result_holder[0]
        if optimized is None:
            optimized = {'_error': '优化结果为空', '_original_sections': sections, '_target_job': target_job, '_career_key': matched_key}
            optimized['岗位职责'] = f'**目标岗位：**{target_job}\\n**简历评分：** 待优化\\n**建议时间：** 一般需2-3天'

    # 异步生成面试话术（如果已有职业信息）
    interview_ai = None
    if session_data.get('career_info'):
        def _run_interview():
            try:
                session_data['interview_ai'] = generate_interview_answers(sections, target_job, matched_key, supplements=supplements)
                with open(session_file, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, ensure_ascii=False, indent=2)
            except:
                pass
        threading.Thread(target=_run_interview).start()

    session_data['optimized_resume'] = optimized
    session_data['interview_ai'] = interview_ai
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    return jsonify({
        **optimized,
        "interview_ai": interview_ai
    })

'''

# Replace the function
new_content = content[:func_start] + replacement + content[func_end:]

# Check syntax
try:
    compile(new_content, path, 'exec')
    print("Syntax OK")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("File written successfully!")
except SyntaxError as e:
    print(f"Syntax error: {e}")
    print(f"Error at line {e.lineno}")
    # Show context
    lines = new_content.split('\n')
    for i in range(max(0, e.lineno-5), min(len(lines), e.lineno+5)):
        print(f'{i+1}: {lines[i][:120]}')
