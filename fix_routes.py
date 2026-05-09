# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# === PLAN ===
# 1. upload_resume ends at line 4680 (return jsonify...)
# 2. Lines 4681-4750 are orphaned inside upload_resume
# 3. @app.route('/api/text-upload') is at line 4752 (inside upload_resume - WRONG!)
# 4. text_upload_resume function starts at line 4756
# 5. _get_ai_job_recommendations starts at line 4941
#
# FIX: 
# - upload_resume: replace lines 4680-4751 with a clean return WITHOUT AI call
# - Remove the rogue @app.route at line 4752 (it's inside upload_resume)
# - Remove the def text_upload_resume wrapper lines (keep the body, remove duplicate def)
# - Actually: keep @app.route + def text_upload_resume as proper top-level route

# Let me first understand: is upload_resume a @app.route function?
# From find_routes output: @app.route at 4400, def at 4408
# upload_resume returns at line 4680
# The @app.route('/api/text-upload') at 4752 is INSIDE upload_resume - that's wrong

# Strategy: 
# 1. Fix upload_resume return: remove AI call, just return immediately
# 2. Remove the orphan lines 4681-4751
# 3. The @app.route('/api/text-upload') at 4752 and def text_upload_resume at 4756
#    need to be moved to BEFORE the orphaned section

# Actually, let me check what line 4752 looks like more carefully
# Line 4752 is @app.route... which should be at sp=0 (top level)
# But it showed sp=0 above - so it's at module level
# But it's AFTER the upload_resume return - so it should work as a separate route

# Wait - if @app.route('/api/text-upload') is at line 4752 (top level)
# and def upload_resume() is at line 4408 (top level)
# and the return of upload_resume is at line 4680
# then the @app.route IS after the function - that's fine for Python

# So the problem is ONLY that:
# 1. upload_resume has synchronous AI call -> fix to background thread
# 2. The orphaned content 4681-4751 is just junk that doesn't matter structurally

# Let me verify: is there anything at line 4752 that matters?
print("\nLine 4752 context:")
for i in range(4748, 4760):
    stripped = lines[i].rstrip()
    print(f"  {i+1} sp={len(lines[i])-len(lines[i].lstrip())}: {repr(stripped)}")

# Check the indentation of @app.route at 4752
route_line = lines[4751]  # 0-indexed
print(f"\n@app.route at line 4752: indent={len(route_line)-len(route_line.lstrip())}")
print(f"Content: {repr(route_line)}")

# Since @app.route is at sp=0, it's a top-level decorator
# It decorates the NEXT def at line 4756
# That's correct - text_upload_resume is its own route

# So the ONLY issue with upload_resume is the AI call blocking
# And with text_upload_resume, the AI call was already fixed (fix_async.py)

# But wait - 500 error on text-upload... 
# Let me check if there's a SyntaxError or RuntimeError from the broken structure
# Let me look at the FULL text_upload_resume function after the fix_async.py changes

print("\nFull text_upload_resume after fix_async:")
for i in range(4751, 4905):
    if lines[i].strip():
        print(f"  {i+1}: {repr(lines[i].rstrip())}")
