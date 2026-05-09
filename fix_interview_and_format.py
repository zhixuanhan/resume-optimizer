# -*- coding: utf-8 -*-
"""全面修复简历优化和面试话术的问题"""
import re

app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"文件大小: {len(content)} 字符")
print(f"文件行数: {content.count(chr(10))} 行")

changes = []

# ========== 修复1: 面试话术 prompt ==========
# 问题1: 标题说"10个"但提醒说"6个"，不一致
# 问题2: max_tokens=3500 可能不够
# 问题3: 需要确保答案足够详细

old_interview_prompt_start = 'prompt = f"""你是一个资深HR面试官。请为应聘【{target_job}】岗位的候选人准备【10个】面试问题及【高度个性化】的答案。'
new_interview_prompt_start = 'prompt = f"""你是一个资深HR面试官。请为应聘【{target_job}】岗位的候选人准备【6个】面试问题及【高度个性化】的答案。每个答案必须包含具体细节，字数不少于150字。'

if old_interview_prompt_start in content:
    content = content.replace(old_interview_prompt_start, new_interview_prompt_start)
    changes.append("✅ 修复面试话术: 标题改为6个")
else:
    changes.append("❌ 未找到面试话术标题")

# 修复面试 max_tokens
if 'max_tokens=3500' in content:
    content = content.replace('max_tokens=3500', 'max_tokens=4500')
    changes.append("✅ 修复面试 max_tokens: 3500 -> 4500")
else:
    changes.append("❌ 未找到面试 max_tokens")

# 修复面试输出数量要求
old_qa_reminder = '必须输出完整的6个问答'
new_qa_reminder = '必须输出完整的6个问答，每个答案都要详细展开，不少于150字'
if old_qa_reminder in content:
    content = content.replace(old_qa_reminder, new_qa_reminder)
    changes.append("✅ 修复: 强调6个问答每个不少于150字")
else:
    changes.append("❌ 未找到6个问答提醒")

# ========== 修复2: 优化经历输出清理函数 ==========
# 在 optimize_experience 函数定义后添加清理函数
# 先找函数结尾

old_exp_return = '''    result = call_ai(prompt, max_tokens=1500, temperature=0.7)
    return result'''

new_exp_return = '''    result = call_ai(prompt, max_tokens=2000, temperature=0.7)
    # 清理多余的标题和空行
    lines = result.split('\\n')
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        line = line.strip()
        # 跳过重复的空行
        if not line:
            if not prev_empty:
                cleaned_lines.append('')
                prev_empty = True
            continue
        prev_empty = False
        # 跳过多余的section标题（如【实习经历】【项目经验】等）
        if re.match(r'^【.+】$', line):
            continue
        cleaned_lines.append(line)
    # 移除开头和结尾的空行
    while cleaned_lines and not cleaned_lines[0].strip():
        cleaned_lines.pop(0)
    while cleaned_lines and not cleaned_lines[-1].strip():
        cleaned_lines.pop()
    return '\\n'.join(cleaned_lines)'''

if old_exp_return in content:
    content = content.replace(old_exp_return, new_exp_return)
    changes.append("✅ 修复: 添加经历输出清理 + max_tokens 1500->2000")
else:
    changes.append("❌ 未找到经历函数return语句")

# ========== 修复3: 个人总结输出清理 ==========
# 在 generate_personal_summary 中也添加清理

old_summary_return_pattern = r"(\s+return result\s*\n\n+)"
def fix_summary_return(m):
    return m.group(0).replace('return result', 'lines = result.split("\\n"); cleaned = [l.strip() for l in lines if l.strip() and not re.match(r"^【.+】$", l.strip())]; return "\\n".join(cleaned)')

# ========== 修复4: 求职意向中的多余 ## 标记 ==========
# 求职意向 hardcoded 内容里有 ##，这些可能是 Markdown 标题标记
# 检查一下是否需要清理

if '## 目标岗位' in content:
    content = content.replace('## 目标岗位', '**目标岗位**')
    changes.append("✅ 修复: 求职意向 ## 改为 **")
else:
    changes.append("ℹ️  求职意向格式正常（无多余##）")

# ========== 修复5: 检查 SyntaxError ==========
# 检查是否有多余的三引号问题
# 查找可能的未闭合三引号
triple_quotes = [m.start() for m in re.finditer(r'"""', content)]
if len(triple_quotes) % 2 != 0:
    changes.append(f"⚠️  警告: 三引号数量为奇数({len(triple_quotes)}个)，可能有未闭合的字符串")
else:
    changes.append(f"✅ 三引号数量正常: {len(triple_quotes)}个")

# 写回文件
with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== 修改结果 ===")
for c in changes:
    print(c)
print(f"\n文件已更新: {app_path}")
