# -*- coding: utf-8 -*-
import urllib.request, json

data = json.dumps({
    'text': '张三，3年Java开发经验，熟悉Spring Boot、MySQL、Redis，负责过电商系统开发，使用Vue做前端，项目获年度最佳。'
}).encode()
req = urllib.request.Request(
    'http://127.0.0.1:5000/api/text-upload',
    data=data,
    headers={'Content-Type': 'application/json'}
)
try:
    r = urllib.request.urlopen(req, timeout=15)
    print(f"Status: {r.status}")
    resp = json.loads(r.read().decode())
    print(f"session_id: {resp.get('session_id')}")
    print(f"sections: {resp.get('sections')}")
    print(f"section_count: {resp.get('section_count')}")
except Exception as e:
    print(f"Error: {e}")