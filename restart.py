# -*- coding: utf-8 -*-
# Kill processes on port 5000 and restart server
import subprocess, time, socket, os

# Kill by PID on port 5000
try:
    result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if ':5000' in line and 'LISTENING' in line:
            parts = line.split()
            if len(parts) >= 5:
                pid = parts[-1]
                print('Killing PID:', pid)
                subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
except Exception as e:
    print('Kill error:', e)

time.sleep(1)

# Start server
server_script = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\run_server.py'
log_file = open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\server.log', 'w')
proc = subprocess.Popen(['python', server_script], 
    stdout=log_file, stderr=subprocess.STDOUT, text=True,
    cwd=r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer')
print('Started PID:', proc.pid)
time.sleep(3)

# Health check
try:
    import urllib.request
    r = urllib.request.urlopen('http://127.0.0.1:5000/', timeout=3)
    print('Server OK! status:', r.status)
except Exception as e:
    print('Server not responding:', e)

print('Done. Log at server.log')