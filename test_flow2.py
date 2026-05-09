import urllib.request, json, time

BASE = 'http://127.0.0.1:5000'
start = time.time()

def post(path, data, timeout=60):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(BASE + path, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        if raw.startswith(b'<'):
            return 'HTML', raw[:300].decode('utf-8', errors='replace')
        return 'JSON', json.loads(raw)

# Full flow test
t0 = time.time()
d1 = post('/api/text-upload', {
    'text': '张三 北京大学光华管理学院2021级 主修市场营销与数据分析 求职行业运营岗位 有字节跳动内容运营实习经验 美团策略运营实习经验 熟练SQL和Python数据分析 有活动策划和KPI达成经验'
})
print('1. text-upload [', d1[0], '] (%.1fs)' % (time.time()-t0))
if d1[0] != 'JSON':
    print('   FATAL:', d1[1][:200]); import sys; sys.exit(1)
sid = d1[1].get('session_id')
print('   session:', sid, '| sections:', d1[1].get('section_count'))

t1 = time.time()
d2 = post('/api/diagnose', {'session_id': sid, 'target_job': '行业运营'})
print('2. diagnose [', d2[0], '] (%.1fs)' % (time.time()-t1))
if d2[0] == 'JSON':
    print('   score:', d2[1].get('score'))
else: print('   HTML ERROR:', d2[1][:100])

t2 = time.time()
d3 = post('/api/career', {'session_id': sid, 'target_job': '行业运营'})
print('3. career [', d3[0], '] (%.1fs)' % (time.time()-t2))
if d3[0] == 'JSON':
    print('   match:', d3[1].get('match_score'))
else: print('   HTML ERROR:', d3[1][:100])

t3 = time.time()
d4 = post('/api/optimize', {'session_id': sid, 'target_job': '行业运营', 'supplements': {}})
print('4. optimize [', d4[0], '] (%.1fs)' % (time.time()-t3))
if d4[0] == 'JSON':
    print('   keys:', list(d4[1].keys()))
    if 'error' in d4[1]: print('   error:', d4[1]['error'])
    # Check specifically what the frontend needs
    if '个人总结' in d4[1]:
        print('   个人总结 (flat):', d4[1]['个人总结'][:80] if d4[1]['个人总结'] else 'EMPTY')
    if '求职意向' in d4[1]:
        print('   求职意向 (flat):', d4[1]['求职意向'][:80] if d4[1]['求职意向'] else 'EMPTY')
    if 'optimized_resume' in d4[1]:
        opt = d4[1]['optimized_resume']
        print('   optimized_resume (nested) keys:', list(opt.keys()) if isinstance(opt, dict) else type(opt))
else:
    print('   HTML ERROR:', d4[1][:200])

print('\nTotal: %.1fs' % (time.time()-start))