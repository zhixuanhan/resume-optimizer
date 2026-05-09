# -*- coding: utf-8 -*-
"""
修复前端：把缺失关键词的点击事件改成打开统一的补充框
"""

filepath = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\templates\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修改 renderCareer 中缺失关键词的点击事件
# 把每个关键词单独的 onclick="openSupplement('xxx')" 改成统一的 onclick="openSupplementModal()"
old_missing = '''if (d.missing_keywords && d.missing_keywords.length) {
        html += `<h3>⚠️ 建议补充的关键词</h3><div style="margin-bottom:1rem">`;
        d.missing_keywords.forEach(k => {
            const supp = supplements[k];
            const cls = supp ? 'tag-green supplemented' : 'tag-red';
            html += `<span class="tag ${cls}" onclick="openSupplement('${k}')" title="点击补充你相关的经历">${k} ${supp ? '✅ 已补充' : '✏️ 点击补充'}</span>`;
        });
        html += `</div>`;
    }'''

new_missing = '''if (d.missing_keywords && d.missing_keywords.length) {
        html += `<h3>⚠️ 建议补充的关键词</h3><div style="margin-bottom:0.5rem">`;
        d.missing_keywords.forEach(k => {
            html += `<span class="tag tag-red">${k}</span>`;
        });
        html += `</div><p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">💡 点击上方的"有更多经历想告诉AI"按钮，补充这些关键词相关的经历！</p>`;
    }'''

if old_missing in content:
    content = content.replace(old_missing, new_missing)
    print("1. 已修改缺失关键词显示区域")
else:
    print("1. 未找到缺失关键词显示区域")

# 2. 删除旧的按关键词补充的函数定义（openSupplement, saveSupplement, closeSupplement, currentSupplementKeyword）
# 这些函数在 supplementPrompts 定义之后

# 先找到并删除旧的函数
old_funcs = '''function openSupplement(keyword) {
    currentSupplementKeyword = keyword;
    document.getElementById('suppKeywordBadge').textContent = keyword;
    const prompt = supplementPrompts[keyword] || `你有没有和「${keyword}」相关的经历？比如工作、实习、项目、比赛、兼职，甚至兴趣爱好都可以！`;
    document.getElementById('suppPrompt').textContent = prompt;
    document.getElementById('supplementInput').value = supplements[keyword] || '';
    document.getElementById('supplementOverlay').classList.add('active');
    document.getElementById('supplementInput').focus();
}

function closeSupplement() {
    document.getElementById('supplementOverlay').classList.remove('active');
    currentSupplementKeyword = null;
}

function saveSupplement() {
    const text = document.getElementById('supplementInput').value.trim();
    if (currentSupplementKeyword) {
        if (text) {
            supplements[currentSupplementKeyword] = text;
        } else {
            delete supplements[currentSupplementKeyword];
        }
    }
    closeSupplement();
    // Re-render career page to update tag styles
    goCareer();
}

// Close modal on overlay click
document.getElementById('supplementOverlay').addEventListener('click', e => {
    if (e.target === document.getElementById('supplementOverlay')) closeSupplement();
});'''

if old_funcs in content:
    content = content.replace(old_funcs, '// 已移除旧的按关键词补充函数，改用统一的 openSupplementModal')
    print("2. 已删除旧的补充函数")
else:
    print("2. 未找到旧的补充函数")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== 前端修复完成 ===")
