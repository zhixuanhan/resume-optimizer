# -*- coding: utf-8 -*-
path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: there are 3 } chars where there should be 1
# Pattern: the text-upload return block ends with:
#     })
# (correct end of return jsonify)
# then some blank lines
# then extra }) (remove this)
# then blank lines
# then def _get_ai_job_recommendations

bad = '''        "job_recommendations": _get_ai_job_recommendations(text[:3000])
    })\n\n\n\n    })\n\n\n\n\n\ndef _get_ai_job_recommendations'''

good = '''        "job_recommendations": _get_ai_job_recommendations(text[:3000])
    })\n\n\ndef _get_ai_job_recommendations'''

if bad in content:
    content = content.replace(bad, good)
    print('Fixed!')
else:
    print('Pattern not found, trying flexible...')
    # Try without exact newlines
    import re
    pattern = r'job_recommendations\(_get_ai_job_recommendationstext\)\[\{:30\}\)\s*\}\)\s*\}\)\s+def _get'
    m = re.search(pattern, content)
    if m:
        print('Found at:', m.start(), '-', m.end())
        print(repr(m.group()))
    else:
        print('Pattern not found either')
        
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
