with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 删掉旧的 except 块（line 426-434，0-indexed 425-433）
# 找到旧 except 开始：line 426 = '    except (urllib.error.URLError...'
# 结束：return f"[AI生成失败: {str(e)}]" 在 line 434，下一个空行在 435

# 找到这些行的索引
for i in range(420, 450):
    print(f'{i+1}: {repr(lines[i])}')

print('---')

# 删除旧 except 块（line 426-434，0-indexed 425-433）
# 保留：return 语句之前的所有内容 + return '[AI生成失败: Unknown error]' 之后的所有内容
# 找 line 426 的索引（0-based = 425）
# 找 return '[AI生成失败: Unknown error]' 之后第一个空行之后的正常内容（应该是 app = Flask）

# 实际上直接删掉 lines[425:434]（旧的 except 到它的 return f）
# 新的 return '[AI生成失败: Unknown error]' 已经在 417行了
del lines[425:434]
print(f'After deletion: total lines = {len(lines)}')

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done')
