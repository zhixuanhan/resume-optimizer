import re

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the if __name__ block
target = "if __name__ == '__main__':"
idx = content.find(target)
if idx < 0:
    print("Not found!")
    exit(1)

print(f"Found at index {idx}")
print("Context:")
print(repr(content[idx:idx+400]))

# Check if already modified
if "PORT = int(os.environ.get" in content:
    print("Already modified!")
else:
    # Add PORT config before if __name__
    port_config = "\n# Railway / Render 端口配置\nPORT = int(os.environ.get('PORT', 5000))\n\n"
    
    # Replace the if __name__ block
    old_block = """if __name__ == '__main__':
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print("=" * 60)
    print("  简历优化助手 已启动!")
    print("  打开浏览器访问: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)"""
    
    new_block = """# Railway / Render 端口配置
PORT = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print("=" * 60)
    print("  简历优化助手 已启动!")
    print(f"  打开浏览器访问: http://127.0.0.1:{PORT}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)"""
    
    if old_block in content:
        content = content.replace(old_block, new_block)
        with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Modified successfully!")
    else:
        print("Old block not found exactly, trying regex...")
        # Try regex
        pattern = r"if __name__ == '__main__':.*?app\.run\([^)]+\)"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            print(f"Found via regex: {repr(match.group())}")
            new_block2 = """# Railway / Render 端口配置
PORT = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print("=" * 60)
    print("  简历优化助手 已启动!")
    print(f"  打开浏览器访问: http://127.0.0.1:{PORT}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)"""
            content = content[:match.start()] + new_block2 + content[match.end():]
            with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
                f.write(content)
            print("Modified via regex!")
        else:
            print("Could not find pattern")
