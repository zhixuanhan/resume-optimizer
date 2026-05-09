# -*- coding: utf-8 -*-
import subprocess, time, socket

# Kill any stray python processes
for pid in [40412, 34804, 32524]:
    try:
        subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True)
    except: pass
time.sleep(1)

# Start fresh
log = open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\server.log', 'w')
proc = subprocess.Popen(
    ['python', r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\run_server.py'],
    stdout=log, stderr=subprocess.STDOUT,
    cwd=r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer'
)
print('PID:', proc.pid)
time.sleep(4)

# Verify
import urllib.request
try:
    r = urllib.request.urlopen('http://127.0.0.1:5000/', timeout=3)
    print('Server UP:', r.status)
except Exception as e:
    print('Server DOWN:', e)