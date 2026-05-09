# -*- coding: utf-8 -*-
"""
修改前端：
1. 把按关键词分别补充 → 改成一个大的"补充经历"文本框
2. 用户自由输入所有想补充的内容
3. 前端把用户输入的整段文字作为 supplements['user_input'] 传给后端
"""

filepath = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\templates\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修改补充提示区域 - 改成一个大按钮
old_hint = '''<!-- 补充引导提示 -->
            <div class="supplement-hint" id="supplementHint">
                <span class="hint-icon">💬</span>
                <div>
                    <strong>点击下方「建议补充的关键词」，告诉我你相关的经历，</strong>
                    优化时会针对性融入，让简历更有竞争力！
                    <br><span style="font-size:0.82rem;opacity:0.8">（不补充也可以直接优化）</span>
                </div>
            </div>'''

new_hint = '''<!-- 补充经历区域 -->
            <div class="supplement-hint" id="supplementHint" style="cursor:pointer" onclick="openSupplementModal()">
                <span class="hint-icon">📝</span>
                <div>
                    <strong style="font-size:1rem">💡 有更多经历想告诉AI？点击这里补充！</strong>
                    <br><span style="font-size:0.85rem;opacity:0.9">你可以把任何相关的经历、项目、技能都写进来，AI会帮你融入简历优化和面试回答中。</span>
                    <br><span id="suppStatus" style="font-size:0.82rem;color:var(--success);margin-top:0.3rem;display:none">✅ 已补充内容</span>
                </div>
            </div>'''

if old_hint in content:
    content = content.replace(old_hint, new_hint)
    print("1. 已修改补充提示区域")
else:
    print("1. 未找到补充提示区域")

# 2. 修改弹窗 HTML - 改成大的补充经历弹窗
old_modal = '''<!-- ===== 补充经历弹窗 ===== -->
<div class="supplement-overlay" id="supplementOverlay">
    <div class="supplement-modal">
        <span class="close-x" onclick="closeSupplement()">&times;</span>
        <h3>💬 补充你的经历</h3>
        <div class="keyword-badge" id="suppKeywordBadge"></div>
        <p id="suppPrompt"></p>
        <textarea id="supplementInput" placeholder="在这里写下你相关的经历...

例如：
我在XX公司实习时做过类似的事情：
• 负责XX客户的拓展和需求对接
• 每月输出行业分析报告，覆盖XX个细分赛道"></textarea>
        <div class="btn-group">
            <button class="btn btn-success" onclick="saveSupplement()">✅ 保存</button>
            <button class="btn btn-outline" onclick="closeSupplement()">取消</button>
        </div>
    </div>
</div>'''

new_modal = '''<!-- ===== 补充经历弹窗 ===== -->
<div class="supplement-overlay" id="supplementOverlay">
    <div class="supplement-modal" style="max-width:650px">
        <span class="close-x" onclick="closeSupplementModal()">&times;</span>
        <h3>📝 补充你的额外经历</h3>
        <p style="font-size:0.9rem;color:var(--text-secondary);margin-bottom:0.75rem">
            把你想到的任何相关经历都写进来，比如：课程项目、兼职经历、社团活动、比赛经验、自学技能等。<br>
            <strong style="color:var(--primary)">AI会根据这些内容帮你优化简历和准备面试回答！</strong>
        </p>
        <textarea id="supplementInput" style="min-height:220px" placeholder="在这里写下你想补充的内容...

例如：
1. 在大学期间参加过"互联网+"大赛，负责市场调研和商业计划书撰写，项目获得省级二等奖
2. 大二暑假在某教育机构做兼职助教，负责学员管理和答疑，培养了良好的沟通能力
3. 自学了Python数据分析，用pandas处理过电商销售数据
4. 在学生会外联部工作过一年，负责拉赞助，成功谈下3家赞助商

提示：写清楚做了什么、有什么成果，AI会帮你润色！"></textarea>
        <div class="btn-group">
            <button class="btn btn-success" onclick="saveSupplementModal()">✅ 保存并继续</button>
            <button class="btn btn-outline" onclick="closeSupplementModal()">取消</button>
        </div>
    </div>
</div>'''

if old_modal in content:
    content = content.replace(old_modal, new_modal)
    print("2. 已修改弹窗 HTML")
else:
    print("2. 未找到弹窗 HTML")

# 3. 修改 JavaScript 函数 - 改成统一的补充函数
old_js = '''// ========== Supplement Modal ==========
const supplementPrompts = {
    '行业研究': '你在学校里有没有做过行业分析、市场调研或研究报告？比如课程论文、商业比赛、社团调研等？','''

new_js = '''// ========== Supplement Modal ==========
// 用户统一补充的内容（不再按关键词分）
let userSupplementText = '';

function openSupplementModal() {
    document.getElementById('supplementInput').value = userSupplementText;
    document.getElementById('supplementOverlay').classList.add('active');
    document.getElementById('supplementInput').focus();
}

function closeSupplementModal() {
    document.getElementById('supplementOverlay').classList.remove('active');
}

function saveSupplementModal() {
    userSupplementText = document.getElementById('supplementInput').value.trim();
    const statusEl = document.getElementById('suppStatus');
    if (userSupplementText) {
        supplements['user_input'] = userSupplementText;
        statusEl.style.display = 'inline';
        statusEl.textContent = '✅ 已补充 ' + userSupplementText.length + ' 字';
    } else {
        delete supplements['user_input'];
        statusEl.style.display = 'none';
    }
    closeSupplementModal();
}

// 点击遮罩关闭
document.getElementById('supplementOverlay').addEventListener('click', e => {
    if (e.target === document.getElementById('supplementOverlay')) closeSupplementModal();
});

// 旧的按关键词补充函数（保留兼容性，但不再使用）
const supplementPrompts = {
    '行业研究': '你在学校里有没有做过行业分析、市场调研或研究报告？比如课程论文、商业比赛、社团调研等？','''

if old_js in content:
    content = content.replace(old_js, new_js)
    print("3. 已修改 JavaScript 函数")
else:
    print("3. 未找到 JavaScript 函数")

# 4. 删除旧的 saveSupplement 和 openSupplement 函数定义（如果存在）
# 这些函数会被上面的新函数覆盖

# 5. 修改 goOptimize 函数中的 supplements 传递 - 确保传递 userSupplementText
old_optimize = '''body: JSON.stringify({
                session_id: sessionId,
                target_job: job,
                supplements: supplements
            })'''

new_optimize = '''body: JSON.stringify({
                session_id: sessionId,
                target_job: job,
                supplements: supplements  // 包含 user_input 键
            })'''

if old_optimize in content:
    content = content.replace(old_optimize, new_optimize)
    print("4. 已确认 optimize 传递 supplements")
else:
    print("4. optimize 传递部分无需修改")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== 前端修改完成 ===")
