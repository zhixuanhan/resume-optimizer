# -*- coding: utf-8 -*-
import urllib.request, json

# First upload
data = json.dumps({
    'text': '张三，3年Java开发经验，熟悉Spring Boot、MySQL、Redis，负责过电商系统开发，使用Vue做前端，项目获年度最佳。'
}).encode()
req = urllib.request.Request(
    'http://127.0.0.1:5000/api/text-upload',
    data=data,
    headers={'Content-Type': 'application/json'}
)
r = urllib.request.urlopen(req, timeout=15)
resp = json.loads(r.read().decode())
session_id = resp['session_id']
print(f"Uploaded, session: {session_id}")

# Now optimize
data2 = json.dumps({
    'session_id': session_id,
    'target_job': 'Java开发工程师',
    'career_goal': '技术专家'
}).encode()
req2 = urllib.request.Request(
    'http://127.0.0.1:5000/api/optimize',
    data=data2,
    headers={'Content-Type': 'application/json'}
)
try:
    r2 = urllib.request.urlopen(req2, timeout=60)
    print(f"Optimize status: {r2.status}")
    resp2 = json.loads(r2.read().decode())
    opt = resp2.get('optimization', {})
    print(f"Key count: {len(opt)}")
    for k, v in opt.items():
        print(f"  {k}: {str(v)[:80]}")
except Exception as e:
    print(f"Error: {e}")