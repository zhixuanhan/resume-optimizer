"""用 dis 反推 career_analysis 字节码缩进"""
import dis, marshal, types, io

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
import importlib.util
spec = importlib.util.spec_from_file_location("app", path)
mod = importlib.util.module_from_spec(spec)

try:
    exec(compile(open(path,'rb').read(), path, 'exec'), mod.__dict__)
except SyntaxError as e:
    print(f'Status: SYNTAX ERROR at line {e.lineno}')
    # 从 app.__dict__ 找 career_analysis
    fn = mod.__dict__.get('career_analysis')
    if fn and hasattr(fn, '__code__'):
        co = fn.__code__
    else:
        print('career_analysis not found in module')
        exit()
else:
    fn = mod.career_analysis
    co = fn.__code__

# 找 career_analysis 的 code object
print(f'Found: {co.co_name}, {co.co_argcount} args')
print(f'First line: {co.co_firstlineno}')

# Disassemble and analyze the bytecode structure
buf = io.StringIO()
dis.dis(fn, file=buf)
lines_out = buf.getvalue().split('\n')

# Find all SETUP_FINALLY (try), POP_EXCEPT/END_FINALLY (except)  
print('\n=== Bytecode structure ===')
for ln in lines_out:
    stripped = ln.strip()
    if stripped.startswith('SETUP_FINALLY') or stripped.startswith('POP_EXCEPT') or \
       stripped.startswith('END_FINALLY') or stripped.startswith('RETURN_VALUE') or \
       stripped.startswith('FOR_ITER') or stripped.startswith('JUMP_ABSOLUTE') or \
       stripped.startswith('POP_JUMP_IF_TRUE') or stripped.startswith('POP_JUMP_IF_FALSE') or \
       'CALL' in stripped or stripped.startswith('LOAD') or stripped.startswith('COMPARE'):
        print(ln)
