# -*- coding: utf-8 -*-
path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove duplicate closing braces
bad = '''    })


    })



def _get_ai_job_recommendations(text):'''

good = '''    })


def _get_ai_job_recommendations(text):'''

if bad in content:
    content = content.replace(bad, good)
    print('Fixed duplicate })')
else:
    print('Not found, trying alternative...')
    # count closing braces
    import re
    # find the text_upload_resume function end
    matches = list(re.finditer(r'def _get_ai_job_recommendations', content))
    if matches:
        idx = matches[0].start()
        segment = content[idx-100:idx]
        print(repr(segment))

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
