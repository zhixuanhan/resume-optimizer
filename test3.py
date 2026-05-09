# -*- coding: utf-8 -*-
# Test each API step individually with very short timeout
import urllib.request, json, sys

BASE = 'http://127.0.0.1:5000'

def test_post(path, data, timeout=5):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(BASE + path, data=body,
                                  headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            content_type = r.headers.get('Content-Type', '')
            raw = r.read()
            if raw.startswith(b'<'):
                return 'HTML', raw[:200].decode('utf-8', errors='replace')
            try:
                return 'JSON', json.loads(raw)
            except:
                return 'TEXT', raw[:200].decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        raw = e.read()
        return 'HTTP' + str(e.code), raw[:200].decode('utf-8', errors='replace')
    except Exception as e:
        return 'ERROR', str(e)[:200]

print('=== STEP 1: text-upload ===')
kind, data = test_post('/api/text-upload', {'text': '张三 北京大学 行业运营 实习经历：字节跳动 负责内容策划'})
print(kind, ':', data)
if kind == 'JSON' and 'session_id' in data:
    sid = data['session_id']
    print('Session:', sid)
    
    print('\n=== STEP 2: diagnose ===')
    kind2, data2 = test_post('/api/diagnose', {'session_id': sid, 'target_job': '行业运营'}, timeout=8)
    print(kind2, ':', data2 if kind2 != 'ERROR' else data2)
    
    print('\n=== STEP 3: career ===')
    kind3, data3 = test_post('/api/career', {'session_id': sid, 'target_job': '行业运营'}, timeout=8)
    print(kind3, ':', data3 if kind3 != 'ERROR' else data3)
    
    print('\n=== STEP 4: optimize ===')
    kind4, data4 = test_post('/api/optimize', {'session_id': sid, 'target_job': '行业运营'}, timeout=8)
    print(kind4, ':', data4 if kind4 != 'ERROR' else data4)
else:
    print('FAIL: text-upload did not return session_id')