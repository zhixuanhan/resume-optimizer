import urllib.request, json, time
BASE = 'http://127.0.0.1:5000'
t0 = time.time()
def post(path, data, timeout=120):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(BASE + path, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        if raw.startswith(b'<'): return 'HTML', raw[:200].decode('utf-8','replace')
        return 'JSON', json.loads(raw)

d1 = post('/api/text-upload', {'text': '张三 北京大学光华管理学院2021级 主修市场营销与数据分析 求职行业运营岗位 有字节跳动内容运营实习经验 美团策略运营实习经验 熟练SQL和Python数据分析 有活动策划和KPI达成经验'})
print('1. text-upload (%.1fs) OK session:%s' % (time.time()-t0, d1[1].get('session_id','')))
sid = d1[1]['session_id']

d2 = post('/api/diagnose', {'session_id': sid, 'target_job': '行业运营'})
print('2. diagnose (%.1fs) score:%s' % (time.time()-t0, d2[1].get('score','')))

d3 = post('/api/career', {'session_id': sid, 'target_job': '行业运营'})
print('3. career (%.1fs) match:%s' % (time.time()-t0, d3[1].get('match_score','')))

d4 = post('/api/optimize', {'session_id': sid, 'target_job': '行业运营', 'supplements': {}})
print('4. optimize (%.1fs) type:%s' % (time.time()-t0, d4[0]))
if d4[0] == 'JSON':
    k = list(d4[1].keys())
    print('   keys:', k)
    for key in ['求职意向','个人总结','实习经历','_career_key']:
        v = d4[1].get(key,'')
        print('   %s: %s' % (key, repr(v[:80]) if isinstance(v,str) else str(v)[:80]))
    if 'error' in d4[1]:
        print('   **ERROR**:', d4[1]['error'])
else:
    print('   FATAL HTML:', d4[1][:200])
print('Total: %.1fs' % (time.time()-t0))