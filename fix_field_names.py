# -*- coding: utf-8 -*-
"""Fix field name mismatch: 职业总结 -> 个人总结"""
import re

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
content = open(path, encoding='utf-8').read()
original = content

# Fix 1: In generate_personal_summary, rename the key from 职业总结 to 个人总结
# The line: optimized['职业总结'] = summary_result
content = content.replace(
    "optimized['职业总结'] = summary_result",
    "optimized['个人总结'] = summary_result"
)
# Also handle the error fallback case
content = content.replace(
    "optimized['职业总结'] = f'[生成失败: {str(ex)}]'",
    "optimized['个人总结'] = f'[生成失败: {str(ex)}]'"
)
# Handle the AI failure fallback
content = content.replace(
    "optimized['职业总结'] = summary_result + '\\n\\n[说明：AI生成失败可用参考职业概要部分字段手工编写个人总结]'",
    "optimized['个人总结'] = summary_result + '\\n\\n[说明：AI生成失败可用参考职业概要部分字段手工编写个人总结]'"
)

# Fix 2: In optimize_resume, wrap response with 'optimization' key
# Find the return statement and change from {**optimized, ...} to {optimization: optimized, ...}
old_return = """    return jsonify({
        **optimized,
        "interview_ai": interview_ai
    })"""
new_return = """    return jsonify({
        "optimization": optimized,
        "interview": interview_ai,
        "career_key": matched_key
    })"""
content = content.replace(old_return, new_return)

# Fix 3: Ensure optimized includes all sections even if AI fails
# The generate_optimized_resume should always return all section keys
# (this is already handled by the existing code - it just adds fallback content)

if content == original:
    print("WARNING: No changes made!")
else:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fix applied successfully!")
    
    # Verify syntax
    import ast
    ast.parse(content)
    print("Syntax OK")
