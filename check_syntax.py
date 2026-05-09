import sys
import ast
import os

os.chdir(r"C:\Users\韩知璇\.qclaw\workspace\resume-optimizer")
try:
    with open("app.py", "r", encoding="utf-8") as f:
        source = f.read()
    ast.parse(source)
    print("Syntax OK")
except SyntaxError as e:
    print("Syntax Error at line %d: %s" % (e.lineno, e.msg))
    if e.text:
        print("Text: %s" % repr(e.text))
except Exception as e:
    print("Error: %s" % e)
