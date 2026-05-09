# -*- coding: utf-8 -*-
# Test the full flow: text upload -> diagnose -> career -> optimize
import urllib.request, json, time

BASE = 'http://127.0.0.1:5000'

def post(path, data, timeout=10):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(BASE + path, data=body, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except Exception as e:
        return 'error', str(e)

# Step 1: text upload
print('Step 1: text upload...')
status, result = post('/api/text-upload', {
    'text': '''张三
求职意向：行业运营
教育经历：北京大学 光华管理学院 2021-2025 GPA 3.8/4.0
实习经历：
- 字节跳动 内容运营 2024.06-2024.09
  负责抖音账号内容策划，平均播放量提升30%，单月增粉5万+
  独立完成10+条短视频脚本撰写，单条最高播放量200万
- 美团 策略运营实习生 2023.12-2024.03
  协助分析用户数据，优化运营策略
项目经验：
- 校园创业项目"校享" 2023.03-2023.12
  校园外卖平台，日均订单200+，覆盖3所高校
技能证书：CET-6(620分)、Python(SQL数据分析)、Excel(数据透视表、VLOOKUP)
'''
}, timeout=30)
print('Status:', status)
if status != 200:
    print('Error:', result)
    print('FAIL: text upload failed')
else:
    session_id = result.get('session_id', result.get('session'))
    print('Session ID:', session_id)
    if not session_id:
        print('FAIL: no session_id returned')
    else:
        # Step 2: diagnose
        print('\nStep 2: diagnose...')
        status2, r2 = post('/api/diagnose', {'session_id': session_id, 'target_job': '行业运营'}, timeout=30)
        print('Status:', status2)
        if status2 != 200:
            print('Error:', r2)
        else:
            print('Score:', r2.get('score'))
            print('Good:', len(r2.get('good', [])), 'items')
            print('Bad:', len(r2.get('bad', [])), 'items')
        
        # Step 3: career
        print('\nStep 3: career...')
        status3, r3 = post('/api/career', {'session_id': session_id, 'target_job': '行业运营'}, timeout=30)
        print('Status:', status3)
        if status3 != 200:
            print('Error:', r3)
        else:
            print('Match score:', r3.get('match_score'))
            print('Missing keywords:', r3.get('missing_keywords', [])[:5])
        
        # Step 4: optimize
        print('\nStep 4: optimize...')
        status4, r4 = post('/api/optimize', {
            'session_id': session_id,
            'target_job': '行业运营',
            'supplements': {}
        }, timeout=30)
        print('Status:', status4)
        if status4 != 200:
            print('Error:', r4)
        else:
            print('Optimized keys:', list(r4.keys()))
            # Check if any key contains HTML or is a string starting with <
            for k, v in r4.items():
                if isinstance(v, str) and v.startswith('<'):
                    print('WARNING: key', k, 'starts with < - HTML response!')
            print('DONE: optimize succeeded')