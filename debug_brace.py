# -*- coding: utf-8 -*-
path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find _get_ai_job_recommendations and look at what's before it
import re
match = re.search(r'def _get_ai_job_recommendations', content)
if match:
    start = max(0, match.start() - 200)
    segment = content[start:match.start()]
    print("--- 200 chars before _get_ai_job_recommendations ---")
    print(repr(segment))
    
    # Count braces in the segment
    opens = segment.count('{')
    closes = segment.count('}')
    print(f"\nBraces in segment: {{ = {opens}, }} = {closes}")
    print(f"Balance: {opens - closes}")
