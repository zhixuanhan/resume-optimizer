# -*- coding: utf-8 -*-
import sys, threading, time
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Fix: remove synchronous AI call from text_upload_resume return
# Replace the return block (lines 4872-4900) with a version that:
# 1. Saves session data immediately
# 2. Spawns background thread for AI recommendations
# 3. Returns quickly

# Find the return block start
for i in range(4870, 4875):
    if '@app.route' in lines[i] or 'def ' in lines[i]:
        print(f"Found next section at {i+1}: {repr(lines[i])}")

print()
print("Lines to fix (4872-4900):")
for i in range(4871, 4901):
    print(f'{i+1}: {repr(lines[i])}')

# The new return block:
new_block = """    # Save session first
    session_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.json")
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    # Background thread for AI job recommendations (non-blocking)
    def bg_recommend(sid, txt):
        try:
            rec = _get_ai_job_recommendations(txt[:3000])
            # Load session and update
            sf = os.path.join(app.config['UPLOAD_FOLDER'], f"{sid}.json")
            with open(sf, 'r', encoding='utf-8') as f2:
                sd = json.load(f2)
            sd['job_recommendations'] = rec
            with open(sf, 'w', encoding='utf-8') as f2:
                json.dump(sd, f2, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[bg_recommend error] {e}")

    threading.Thread(target=bg_recommend, args=(session_id, text), daemon=True).start()

    return jsonify({
        "session_id": session_id,
        "filename": "text input",
        "text_preview": text[:2000] + ("..." if len(text) > 2000 else ""),
        "sections": {k: (v[:500] + "..." if len(v) > 500 else v) for k, v in sections.items()},
        "section_count": len([v for v in sections.values() if len(v) > 20]),
        "job_recommendations": []  # Will be populated in background
    })
"""

# Replace lines 4872-4900 (0-indexed: 4871-4899)
# We need to replace lines 4872 to 4900 (inclusive), 0-indexed = 4871 to 4899
old_start = 4871
old_end = 4900  # inclusive, 0-indexed = line 4900 = index 4899

print(f"\nReplacing lines {old_start+1}-{old_end} (indexes {old_start}-{old_end-1})")

# Build new lines
new_lines = lines[:old_start] + [new_block + '\n'] + lines[old_end:]

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Done!")
# Verify syntax
with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8', errors='replace') as f:
    lines2 = f.readlines()
for i in range(4871, 4910):
    if i < len(lines2) and lines2[i].strip():
        print(f'{i+1}: {repr(lines2[i])}')
