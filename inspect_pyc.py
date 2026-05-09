"""直接从字节码重建 career_analysis 函数源码"""
import dis, marshal, struct, types

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'

# 读取 .pyc 文件获取字节码
pyc_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\__pycache__\app.cpython-312.pyc'
try:
    with open(pyc_path, 'rb') as f:
        # Skip .pyc header (16 bytes for Python 3.12+)
        f.read(16)
        code = marshal.load(f)
    print(f"Marshal load OK, code type: {type(code)}")
    print(f"Constants: {[c for c in code.co_consts if isinstance(c, types.CodeType)][:5]}")
    # Find career_analysis code object
    for const in code.co_consts:
        if isinstance(const, types.CodeType) and 'career' in const.co_name:
            print(f"Found: {const.co_name}, argcount={const.co_argcount}")
            # Disassemble
            import io
            buf = io.StringIO()
            dis.dis(const, file=buf)
            print(buf.getvalue()[:2000])
except Exception as e:
    print(f"Error: {e}")
    import traceback; traceback.print_exc()