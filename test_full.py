import urllib.request, json, time

BASE = 'http://127.0.0.1:5000'
start = time.time()

def post(path, data, timeout=60):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(BASE + path, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

# Step 1: text upload
d1 = post('/api/text-upload', {'text': '张三 北京大学光华管理学院2021级 求职行业运营 字节跳动实习内容策划 美团策略运营 SQL Python数据分析 熟悉运营方法论 有KPI达成经验'})
sid = d1.get('session_id')
print('1. text-upload OK (%.1fs) session:%s' % (time.time()-start, sid))

# Step 2: diagnose
d2 = post('/api/diagnose', {'session_id': sid, 'target_job': '行业运营'})
print('2. diagnose OK (%.1fs) score:%s good:%d bad:%d' % (time.time()-start, d2.get('score'), len(d2.get('good',[])), len(d2.get('bad',[]))))

# Step 3: career
d3 = post('/api/career', {'session_id': sid, 'target_job': '行业运营'})
print('3. career OK (%.1fs) match:%s' % (time.time()-start, d3.get('match_score')))
print('   missing:', d3.get('missing_keywords', [])[:3])

# Step 4: optimize
d4 = post('/api/optimize', {'session_id': sid, 'target_job': '行业运营', 'supplements': {}})
print('4. optimize OK (%.1fs) keys:%s' % (time.time()-start, list(d4.keys())))
if 'error' in d4:
    print('   ERROR:', d4['error'])
else:
    print('   summary length:', len(d4.get('personal_summary','')))
    print('   experiences count:', len(d4.get('experiences', [])))

print('Total: %.1fs' % (time.time()-start))