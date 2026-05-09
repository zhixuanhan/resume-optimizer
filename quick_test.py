# -*- coding: utf-8 -*-
import urllib.request, json, time, urllib.error

url = 'http://127.0.0.1:5000/api/text-upload'
# 长文本，50字符以上
payload = {
    'text': '张三，北京大学计算机科学与技术专业本科毕业，具有3年互联网产品工作经验，曾在腾讯担任高级产品经理，负责微信小程序及移动端产品的规划、设计与运营，拥有丰富的数据分析和用户增长经验，精通Python、Java和SQL，熟悉机器学习基础。'
}
data = json.dumps(payload).encode()
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
start = time.time()
try:
    resp = urllib.request.urlopen(req, timeout=15)
    elapsed = time.time() - start
    result = json.loads(resp.read().decode())
    print('SUCCESS! Time: {:.1f}s'.format(elapsed))
    print('Session: {}'.format(result.get('session_id')))
    print('Section count: {}'.format(result.get('section_count')))
    sid = result.get('session_id')
    print('Recommendations: {}'.format(type(result.get('job_recommendations'))))
    
    # Test /api/diagnose
    if sid:
        url2 = 'http://127.0.0.1:5000/api/diagnose'
        payload2 = json.dumps({'session_id': sid, 'target_job': '产品经理'}).encode()
        req2 = urllib.request.Request(url2, data=payload2, headers={'Content-Type': 'application/json'})
        start2 = time.time()
        try:
            resp2 = urllib.request.urlopen(req2, timeout=120)
            elapsed2 = time.time() - start2
            result2 = json.loads(resp2.read().decode())
            print('\nDiagnose OK! Time: {:.1f}s'.format(elapsed2))
            print('Status: {}'.format(result2.get('status')))
            print('Score: {}'.format(result2.get('score')))
        except urllib.error.HTTPError as e:
            print('Diagnose HTTP {}: {}'.format(e.code, e.read().decode()))
        except Exception as e:
            print('Diagnose Error: {}'.format(e))
    
except urllib.error.HTTPError as e:
    print('HTTP {}: {}'.format(e.code, e.read().decode()))
except Exception as e:
    print('Error: {}'.format(e))
