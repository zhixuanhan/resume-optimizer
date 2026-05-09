# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:\Users\韩知璇\.qclaw\workspace\resume-optimizer")
from app import app
import waitress
print("简历优化助手 已启动!")
print("打开浏览器访问: http://127.0.0.1:5000")
waitress.serve(app, host='127.0.0.1', port=5000, threads=4)
