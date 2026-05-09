# -*- coding: utf-8 -*-
"""测试面试话术功能"""
import urllib.request, json, time

# Step 1: Upload a resume with more details
resume_text = """
张三
电话：13800138000
邮箱：zhangsan@email.com

教育经历：
2020-2024 北京大学 计算机科学与技术 本科
主修课程：数据结构、算法、操作系统、计算机网络、数据库原理

实习经历：
2023.06-2023.09 字节跳动 抖音产品经理实习生
- 负责抖音创作者工具的用户调研，访谈了50+创作者
- 参与A/B测试设计，优化发布流程，提升发布转化率12%
- 使用SQL分析用户行为数据，输出3份数据报告

2022.07-2022.09 腾讯 微信产品运营实习生
- 运营微信公众号，粉丝增长2000+
- 策划并执行2场线上活动，参与人数500+

项目经历：
2023.03-2023.06 校园二手交易平台（课程设计）
- 作为产品负责人，完成需求分析、原型设计
- 协调3人团队，按时交付产品
- 上线后获得500+用户

技能证书：
- 熟练使用SQL、Python进行数据分析
- 掌握Axure、Figma等原型工具
- CET-6 (580分)
- 国家计算机二级证书
"""

data = json.dumps({'text': resume_text}).encode()
req = urllib.request.Request('http://127.0.0.1:5000/api/text-upload', data=data, headers={'Content-Type': 'application/json'})
r = urllib.request.urlopen(req, timeout=30)
resp = json.loads(r.read())
session_id = resp['session_id']
print(f'Upload OK: session_id={session_id}')
print(f'Sections: {list(resp.get("sections", {}).keys())}')

# Step 2: Call optimize
opt_data = json.dumps({
    'session_id': session_id,
    'target_job': '产品经理',
    'supplements': {}
}).encode()
opt_req = urllib.request.Request('http://127.0.0.1:5000/api/optimize', data=opt_data, headers={'Content-Type': 'application/json'})
opt_r = urllib.request.urlopen(opt_req, timeout=200)
opt_resp = json.loads(opt_r.read())

print(f'\nOptimize OK')
print(f'Keys: {list(opt_resp.keys())}')

if 'interview_ai' in opt_resp:
    interview = opt_resp['interview_ai']
    if interview:
        # Count Q&A pairs
        q_count = interview.count('Q')
        print(f'\n面试话术字符数: {len(interview)}')
        print(f'问题数量(Q出现次数): {q_count}')
        print('\n前800字符预览:')
        print(interview[:800])
    else:
        print('interview_ai is empty')
else:
    print('No interview_ai field')
