# -*- coding: utf-8 -*-
# Live test with proper content length
import urllib.request, json, time

BASE = 'http://127.0.0.1:5000'
start = time.time()

def post(path, data, timeout=60):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(BASE + path, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        ct = r.headers.get('Content-Type', '')
        raw = r.read()
        if raw.startswith(b'<') or raw.startswith(b'\n<'):
            return 'HTML', raw[:300].decode('utf-8', errors='replace')
        return 'JSON', json.loads(raw)

# Step 1: text upload (long text, >50 chars)
d1 = post('/api/text-upload', {
    'text': '张三 北京大学光华管理学院2021级学生 主修市场营销与数据分析 求职行业运营岗位 有字节跳动内容运营实习经验 美团策略运营实习经验 熟练掌握SQL和Python进行数据分析 有活动策划和KPI达成经验 熟悉运营方法论和用户增长策略'
})
t1 = time.time() - start
print('1. text-upload [%s] (%.1fs) type:%s' % (d1[0], t1, d1[0]))
if d1[0] == 'JSON':
    sid = d1[1].get('session_id')
    print('   session:%s section_count:%s' % (sid, d1[1].get('section_count')))
    if sid:
        # Step 2
        d2 = post('/api/diagnose', {'session_id': sid, 'target_job': '行业运营'})
        t2 = time.time() - start
        print('2. diagnose [%s] (%.1fs) type:%s score:%s' % (d2[0], t2, d2[0], d2[1].get('score') if d2[0]=='JSON' else d2[0]))
        
        # Step 3
        d3 = post('/api/career', {'session_id': sid, 'target_job': '行业运营'})
        t3 = time.time() - start
        print('3. career [%s] (%.1fs) type:%s match:%s' % (d3[0], t3, d3[0], d3[1].get('match_score') if d3[0]=='JSON' else d3[0]))
        
        # Step 4
        d4 = post('/api/optimize', {'session_id': sid, 'target_job': '行业运营', 'supplements': {}})
        t4 = time.time() - start
        print('4. optimize [%s] (%.1fs) type:%s' % (d4[0], t4, d4[0]))
        if d4[0] == 'JSON':
            keys = list(d4[1].keys())
            print('   keys:', keys)
            if 'error' in d4[1]:
                print('   error:', d4[1]['error'][:100])
        else:
            print('   body:', d4[1][:200])
else:
    print('   body:', str(d1[1])[:200])

print('\nTotal: %.1fs' % (time.time()-start))