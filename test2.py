import urllib.request, json, time

BASE = 'http://127.0.0.1:5000'

# Test text upload with short timeout
print('Testing text upload...')
data = json.dumps({'text': '张三 测试'}).encode('utf-8')
req = urllib.request.Request(BASE + '/api/text-upload', data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req, timeout=5) as r:
        print('text-upload status:', r.status)
except Exception as e:
    print('text-upload error:', e)

# Test diagnose with session from earlier
print('\nTesting diagnose with session e1852b04...')
data2 = json.dumps({'session_id': 'e1852b04', 'target_job': '行业运营'}).encode('utf-8')
req2 = urllib.request.Request(BASE + '/api/diagnose', data=data2, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req2, timeout=10) as r:
        print('diagnose status:', r.status)
        body = r.read()
        if body.startswith(b'<'):
            print('HTML response! First 200:', body[:200])
        else:
            print('Response:', body[:500])
except Exception as e:
    print('diagnose error:', e)