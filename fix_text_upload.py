# -*- coding: utf-8 -*-
path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the wrongly inserted block (inserted inside return statement)
bad = '''        "job_recommendations": _get_ai_job_recommendations(text[:3000])

@app.route('/api/text-upload', methods=['POST'])
def text_upload_resume():
    """directly accept text resume, no PDF needed"""
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({"error": "please provide resume text"}), 400

    text = data['text'].strip()
    if len(text) < 50:
        return jsonify({"error": "resume too short, need at least 50 chars"}), 400

    session_id = str(uuid.uuid4())[:8]
    sections = parse_resume_sections(text)

    session_data = {
        "session_id": session_id,
        "filename": "text input",
        "filepath": "",
        "raw_text": text,
        "sections": sections,
        "target_job": "",
        "diagnosis": None,
        "career_info": None,
        "optimized_resume": None
    }

    session_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.json")
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    return jsonify({
        "session_id": session_id,
        "filename": "text input",
        "text_preview": text[:2000] + ("..." if len(text) > 2000 else ""),
        "sections": {k: (v[:500] + "..." if len(v) > 500 else v) for k, v in sections.items()},
        "section_count": len([v for v in sections.values() if len(v) > 20]),
        "job_recommendations": _get_ai_job_recommendations(text[:3000])
    })

'''

good = '''        "job_recommendations": _get_ai_job_recommendations(text[:3000])
    })


@app.route('/api/text-upload', methods=['POST'])
def text_upload_resume():
    """directly accept text resume, no PDF needed"""
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({"error": "please provide resume text"}), 400

    text = data['text'].strip()
    if len(text) < 50:
        return jsonify({"error": "resume too short, need at least 50 chars"}), 400

    session_id = str(uuid.uuid4())[:8]
    sections = parse_resume_sections(text)

    session_data = {
        "session_id": session_id,
        "filename": "text input",
        "filepath": "",
        "raw_text": text,
        "sections": sections,
        "target_job": "",
        "diagnosis": None,
        "career_info": None,
        "optimized_resume": None
    }

    session_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.json")
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    return jsonify({
        "session_id": session_id,
        "filename": "text input",
        "text_preview": text[:2000] + ("..." if len(text) > 2000 else ""),
        "sections": {k: (v[:500] + "..." if len(v) > 500 else v) for k, v in sections.items()},
        "section_count": len([v for v in sections.values() if len(v) > 20]),
        "job_recommendations": _get_ai_job_recommendations(text[:3000])
    })


'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('FIXED')
else:
    print('BAD BLOCK NOT FOUND')
