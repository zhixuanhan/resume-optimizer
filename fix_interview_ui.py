# -*- coding: utf-8 -*-
import re

file_path = r"C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\templates\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 新的 renderInterview 函数 - 优先使用AI生成的个性化话术
new_function = r"""function renderInterview(d) {
    const el = document.getElementById('interviewContent');

    // 优先使用AI生成的个性化面试话术（来自 /api/optimize 的返回）
    const aiAnswers = d.interview_ai || d.interview_answers;
    if (aiAnswers && aiAnswers.trim()) {
        // AI返回的是纯文本格式 "Q1: ...\nA1: ...\nQ2: ..."
        // 用正则解析成 HTML 显示
        let html = '<h3 style="margin-bottom:1rem">🎤 AI个性化面试话术</h3>';
        html += '<div class="ai-interview-note">以下答案结合您的真实经历定制，请根据实际情况调整</div>';
        
        // 把整个文本按 Q1: Q2: ... 分割
        const qaBlocks = aiAnswers.split(/(?=Q\d+:)/g).filter(b => b.trim());
        
        qaBlocks.forEach(block => {
            block = block.trim();
            if (!block) return;
            // 分割问题和答案 - 找 A数字: 的位置
            const qPartMatch = block.match(/Q(\d+):?\s*([\s\S]*?)$/);
            if (!qPartMatch) return;
            
            const qNum = qPartMatch[1];
            let restText = qPartMatch[2];
            
            // 在剩余文本中找 A数字: 的位置
            const aMatch = restText.match(/A\d+:\s*([\s\S]*?)$/i);
            let qText = restText;
            let aText = '';
            
            if (aMatch) {
                aText = aMatch[1].trim();
                qText = restText.substring(0, restText.indexOf(aMatch[0])).trim();
            }
            
            html += '<div class="qa-item">';
            html += '<div class="question">Q' + qNum + ': ' + qText.replace(/^Q\d+:?\s*/, '') + '</div>';
            html += '<div class="answer">' + aText + '</div>';
            html += '</div>';
        });
        
        el.innerHTML = html;
        return;
    }

    // 如果没有AI话术，fallback到静态话术库
    const careerKey = d._career_key;
    if (!careerKey) { el.innerHTML = '<p>暂无面试话术数据</p>'; return; }
    fetch('/api/career', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ session_id: sessionId, target_job: d._target_job })
    }).then(r => r.json()).then(cd => {
        if (cd.interview_qa && cd.interview_qa.length) {
            let html = '<h3 style="margin-bottom:1rem">🎤 面试高频问题 & 建议回答</h3>';
            cd.interview_qa.forEach((qa, i) => {
                html += '<div class="qa-item">\
                    <div class="question">Q' + (i+1) + ': ' + qa.q + '</div>\
                    <div class="answer">' + qa.a + '</div>\
                </div>';
            });
            el.innerHTML = html;
        } else {
            el.innerHTML = '<p>暂无面试话术数据</p>';
        }
    });
}"""

# 替换旧的 renderInterview 函数
old_start = "function renderInterview(d) {"
old_end = "// ========== Copy Resume"

start_idx = content.find(old_start)
end_idx = content.find(old_end)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_function + "\n\n" + content[end_idx:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed renderInterview!")
else:
    print("Could not find function boundaries")