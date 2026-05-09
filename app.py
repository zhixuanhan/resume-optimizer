# -*- coding: utf-8 -*-







"""







简历优化助手 Web 应用







功能：上传PDF简历 → 简历诊断 → 岗位分析 → 职业规划 → 简历优化 → 下载 + 面试话术







"""















import os







import re







import json







import uuid
import threading







import urllib.request







import urllib.error







from datetime import datetime







from flask import Flask, render_template, request, jsonify, send_file







from PyPDF2 import PdfReader







try:



    import pdfplumber



    HAS_PDFPLUMBER = True



except ImportError:



    HAS_PDFPLUMBER = False















# ============================================================







# AI 配置(硅基流动 SiliconFlow)







# ============================================================







# 优先使用环境变量，fallback 到空字符串（生产环境应设置环境变量）
SILICONFLOW_API_KEY = os.environ.get('SILICONFLOW_API_KEY', 'sk-daelfpmifygniemtcluyiigmawqmouzrnesyrfkovhqmbgwg')

if not SILICONFLOW_API_KEY:
    print("⚠️ 警告: SILICONFLOW_API_KEY 环境变量未设置")







SILICONFLOW_MODEL = 'Qwen/Qwen3-8B'  # 快速模型























def call_ai(prompt, max_tokens=1500, temperature=0.7):







    """调用硅基流动 API 生成内容"""







    url = 'https://api.siliconflow.cn/v1/chat/completions'







    payload = {







        'model': SILICONFLOW_MODEL,







        'messages': [{'role': 'user', 'content': prompt}],







        'temperature': temperature,







        'max_tokens': max_tokens







    }







    data = json.dumps(payload).encode('utf-8')







    req = urllib.request.Request(url, data=data, headers={







        'Authorization': f'Bearer {SILICONFLOW_API_KEY}',







        'Content-Type': 'application/json'







    })







    for attempt in range(2):







        try:







            with urllib.request.urlopen(req, timeout=180) as resp:







                result = json.loads(resp.read())







                return result['choices'][0]['message']['content'].strip()







        except TimeoutError:







            if attempt == 0:







                continue  # 重试一次







            return '[AI生成失败: The read operation timed out]'
        except urllib.error.HTTPError as e:
            return f'[AI生成失败: HTTP错误 {e.code}]'
        except Exception as e:
            return f'[AI生成失败: {str(e)}]'







        except Exception as e:







            return f'[AI生成失败: {str(e)}]'















    return '[AI生成失败: Unknown error]'























app = Flask(__name__)







app.config['UPLOAD_FOLDER'] = 'uploads'







app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024







app.secret_key = 'resume_optimizer_2026_qclaw'















os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)















# ============================================================







# 工具函数







# ============================================================















def extract_text_from_pdf(pdf_path):



    """Dual PDF parsing to maximize text extraction"""



    texts = []



    



    # Method 1: PyPDF2



    try:



        reader = PdfReader(pdf_path)



        for i, page in enumerate(reader.pages):



            pt = page.extract_text()



            if pt and pt.strip():



                texts.append(f"[page{i+1}]\n{pt}")



    except Exception:



        pass



    



    # Method 2: pdfplumber (better at tables and layout)



    if HAS_PDFPLUMBER:



        try:



            with pdfplumber.open(pdf_path) as pdf:



                for i, page in enumerate(pdf.pages):



                    t = page.extract_text()



                    if t and t.strip():



                        if t.strip() not in "\n".join(texts):



                            texts.append(f"[page{i+1}]\n{t}")



                    tables = page.extract_tables()



                    for table in tables:



                        if table:



                            rows = [",".join([str(c or "").strip() for c in row]) for row in table if any(c for c in row)]



                            if rows:



                                texts.append("[table]\n" + "\n".join(rows))



        except Exception:



            pass



    



    if not texts:



        return "[PDF parse failed - please check the file]"



    



    combined = "\n".join(texts)



    # Remove control characters



    combined = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", combined)



    return combined.strip()











def extract_json(s):



    """Extract JSON from AI response, handle markdown code blocks"""



    if not s:



        return None



    # Strip markdown code fences



    s = re.sub(r"^```(?:json)?\s*", "", s.strip(), flags=re.IGNORECASE | re.MULTILINE)



    s = re.sub(r"\s*```$", "", s.strip())



    start = s.find("{")



    end = s.rfind("}")



    if start == -1 or end == -1 or end <= start:



        return None



    raw = s[start:end+1]



    try:



        return json.loads(raw)



    except json.JSONDecodeError:



        pass



    # Fix fullwidth quotes



    raw = raw.replace("\u201c", '"').replace("\u201d", '"').replace("\u300c", '"').replace("\u300d", '"')



    # Fix single-quote keys



    raw = re.sub(r"'([^']*?)'\s*:", r'"\1":', raw)



    # Fix single-quote values



    def fix_sq(m):



        inner = m.group(1)



        inner = inner.replace('\\"', '@@DBL@@').replace("'", "\\'").replace('@@DBL@@', '\\"')



        return '"' + inner + '"'



    raw = re.sub(r":\s*'([^']*)'", fix_sq, raw)



    # Fix trailing commas



    raw = re.sub(r",\s*([}\]])", r"\1", raw)



    try:



        return json.loads(raw)



    except:



        return None







def parse_resume_sections(text):







    sections = {}







    patterns = {







        '个人信息': r'(?:个人[信息概况]|基本信息|姓名|联系方式)',







        '求职意向': r'(?:求职意向|应聘岗位|目标岗位|职业诉求|职业偏好)',







        '教育经历': r'(?:教育经历|教育背景|学历|毕业院校)',







        '实习经历': r'(?:实习经历|工作经历|实践经历|项目经验|工作履历)',







        '项目经验': r'(?:项目经验|项目经历|科研项目|竞赛)',







        '校园经历': r'(?:校园经历|社团活动|学生工作|课外活动)',







        '技能证书': r'(?:技能|证书|专业技能|技术能力|语言能力|获奖情况|荣誉)',







        '自我评价': r'(?:自我评价|个人总结|个人优势|关于我|简介)',







    }







    lines = text.split('\n')







    current_section = '其他'







    sections[current_section] = []







    for line in lines:







        s = line.strip()







        if not s:







            continue







        matched = None







        for sn, pat in patterns.items():







            if re.search(pat, s, re.IGNORECASE):







                matched = sn







                break







        if matched:







            current_section = matched







            if current_section not in sections:







                sections[current_section] = []







            sections[current_section].append(s)







        else:







            if current_section not in sections:







                sections[current_section] = []







            sections[current_section].append(s)







    return {k: '\n'.join(v).strip() for k, v in sections.items()}























def diagnose_resume(sections, target_job=""):


    try:


        all_text = '\n'.join(f"【{k}】\n{sections[k]}" for k in sections if sections.get(k))


        prompt = (


            f"你是一位资深HR和猎头，请对以下简历进行评分(0-100分)和详细诊断。\n\n"


            f"目标岗位：{target_job or '未指定'}\n\n"


            f"简历内容：\n{all_text[:3000]}\n\n"


            '请以详细JSON格式回复(只输出JSON，不要其他内容)：\n'


            '{"score":分数,"good":["优点1","优点2"],"bad":["不足1","不足2"],"suggestions":["建议1","建议2"]}'


        )


        result = call_ai(prompt, max_tokens=800, temperature=0.3)


        parsed = extract_json(result)


        if parsed:


            return parsed


        return {"score": 50, "good": ["简历结构完整"], "bad": ["AI诊断解析失败，请重试"], "suggestions": ["可尝试重新上传或刷新页面"]}


    except Exception as e:


        return {"score": 50, "good": ["简历已上传"], "bad": [f"诊断失败: {str(e)[:50]}"], "suggestions": ["请检查网络后重试"]}


def get_job_keywords(job_name):







    """获取岗位相关关键词"""







    keyword_map = {







        "行业运营": ["行业研究", "B端", "客户拓展", "数据分析", "行业方案", "BD", "GMV", "商业化", "竞品分析", "用户增长"],







        "商业化运营": ["变现", "营收", "GMV", "ARPU", "定价策略", "广告", "付费转化", "流量变现", "商业化", "收入增长"],







        "品牌营销": ["品牌策划", "品牌传播", "市场推广", "品牌定位", "营销活动", "媒介投放", "KOL", "品牌声量"],







        "广告投放": ["信息流", "SEM", "SEO", "ROI", "CTR", "CPC", "千川", "巨量引擎", "投放策略", "素材优化"],







        "用户增长": ["增长策略", "AARRR", "获客", "留存", "裂变", "用户生命周期", "转化率", "增长实验", "数据驱动"],







        "产品经理": ["需求分析", "PRD", "原型设计", "用户调研", "迭代", "MVP", "数据埋点", "跨部门协作", "产品规划"],







        "内容运营": ["内容策划", "文案写作", "选题", "爆款", "阅读量", "粉丝增长", "内容分发", "新媒体", "图文/短视频"],







        "活动运营": ["活动策划", "执行落地", "资源协调", "活动复盘", "参与人数", "转化效果", "线上/线下活动"],







    }







    for key, kws in keyword_map.items():







        if key in job_name or any(a in job_name for a in keyword_map.keys()):







            return kws







    return ["运营", "策划", "执行", "数据分析", "项目管理", "沟通协调"]























# ============================================================







# 职业数据库







# ============================================================















CAREER_DB = {







    "行业运营": {







        "aliases": ["行业运营", "行业运营专员", "行业运营经理", "垂直行业运营"],







        "salary_bj": {







            "junior": {"range": "10K-18K", "avg": "14K", "note": "0-2年经验，本科"},







            "mid": {"range": "18K-30K", "avg": "24K", "note": "3-5年经验，有成功案例"},







            "senior": {"range": "30K-50K+", "avg": "40K", "note": "5年+，带团队/负责完整业务线"}







        },







        "market_analysis": {







            "demand": "🔥 高需求 — 电商、SaaS、本地生活、企业服务都需要",







            "supply": "⚖️ 供给中等 — 懂特定行业的复合型人才稀缺",







            "difficulty": "⭐⭐⭐ 中等偏难 — 需要行业知识+运营能力双重积累",







            "trend": "📈 上升趋势 — 企业精细化运营，垂直行业深耕是方向",







            "key_employers": ["美团/字节(本地生活)", "阿里(1688/钉钉)", "腾讯(企业服务)", "SaaS创业公司", "各行业头部企业运营部"]







        },







        "daily_work": [







            "研究目标行业的发展趋势、竞争格局和玩家生态",







            "制定行业解决方案和运营策略(如何帮客户赚钱)",







            "BD拓展行业客户，维护关键客户关系",







            "策划行业营销活动(峰会、沙龙、白皮书等)",







            "监控行业核心指标(GMV、活跃商户数、复购率等)",







            "输出行业洞察报告，为产品和战略提供输入"







        ],







        "dev_path": [







            {"level": "L1 入门期 (0-1年)", "title": "行业运营专员",







             "tasks": ["熟悉行业生态和竞品格局", "执行基础运营活动和客户跟进", "撰写数据日报/周报", "协助BD做客户资料整理"],







             "skills": ["Excel透视表/VLOOKUP", "基础商务文案", "行业知识快速学习", "会议纪要和跟进"],







             "salary": "10-14K", "action": "先入行，选一个你感兴趣的行业深扎"},







            {"level": "L2 成长期 (1-3年)", "title": "行业运营经理",







             "tasks": ["独立负责一个细分行业/品类的运营", "策划并执行行业营销全案", "跨部门协调产研/销售/市场资源", "对GMV或用户增长指标负责"],







             "skills": ["SQL取数和分析", "项目管理(排期/风险/交付)", "商务谈判和演示", "行业深度报告撰写"],







             "salary": "18-28K", "action": "争取独立负责一条线，积累可量化的业绩"},







            {"level": "L3 进阶期 (3-5年)", "title": "高级行业运营/行业负责人",







             "tasks": ["负责整个行业线战略规划和P&L", "搭建行业解决方案体系(可复制)", "带领3-8人团队", "向总监/VP汇报"],







             "skills": ["战略思维和商业敏感度", "团队管理和培养", "财务建模(ROI测算)", "高层汇报和讲故事"],







             "salary": "30-45K", "action": "从执行者转向管理者，建立方法论"},







            {"level": "L4 专家期 (5年+)", "title": "行业运营总监/VP",







             "tasks": ["管理多条行业线", "参与公司级战略决策", "行业影响力建设(演讲/文章)", "0到1孵化新业务"],







             "skills": ["投资人思维", "资源整合与生态建设", "公众演讲和个人品牌", "组织设计与变革管理"],







             "salary": "50-80K+ 股权", "action": "成为行业KOL，考虑创业或合伙人路线"}







        ],







        "competencies": ["行业研究与洞察", "B端客户理解", "数据分析能力", "活动策划与执行", "跨部门协作", "商业化/GMV思维"],







        "interview_qa": [







            {"q": "你为什么想做行业运营？", "a": "我喜欢深入研究一个领域，找到其中的规律和机会。行业运营既能让我持续学习新行业，又能用运营手段创造实际商业价值。比如在XX项目中，我通过分析行业痛点设计了XX方案，最终带来了XX结果。"},







            {"q": "你怎么理解这个行业运营的价值？", "a": "我认为行业运营是连接'平台能力'和'行业需求'的桥梁。一方面深入理解行业客户的痛点和场景，另一方面把平台的产品能力翻译成客户能理解的解决方案。核心价值是：帮客户赚到钱，同时帮平台拿到市场份额。"},







            {"q": "如果让你负责一个全新行业，你会怎么入手？", "a": "我会分四步：①先用1-2周做行业扫盲——看报告、访谈客户、体验竞品；②画出行业地图(玩家、链条、痛点)；③找3-5个标杆客户深度合作，跑通MVP；④基于MVP结果复制推广。关键是先小步快跑验证，再规模化。"},







            {"q": "你的数据分析能力怎么样？", "a": "我熟练使用Excel透视表和常用函数，能独立完成日报/周报的数据整理。目前在自学SQL，已经能用基本查询取数。我相信数据不是目的而是工具——关键是从数据中发现问题、指导行动。"},







            {"q": "你觉得你最大的优势是什么？短板呢？", "a": "最大优势是我学习和适应快，而且不惧怕从零开始——之前XX项目我就是从零搭起来的。短板是目前行业深度还不够深，但这也是我最想在这个岗位上弥补的，我计划入职后前3个月集中攻克目标行业知识。"}







        ]







    },







    "商业化运营": {







        "aliases": ["商业化运营", "商业化专员", "变现运营", "商业化经理", "营收运营"],







        "salary_bj": {







            "junior": {"range": "12K-20K", "avg": "16K", "note": "0-2年，有变现意识优先"},







            "mid": {"range": "20K-35K", "avg": "28K", "note": "3-5年，有从0到1变现经验"},







            "senior": {"range": "35K-55K+", "avg": "45K", "note": "5年+，负责过千万级营收线"}







        },







        "market_analysis": {







            "demand": "🔥🔥 很高需求 — 所有互联网公司都需要变现人才",







            "supply": "⚖️ 供给偏少 — 有实战变现经验的候选人稀缺",







            "difficulty": "⭐⭐⭐⭐ 较难 — 需要数据敏感+商业意识+执行力",







            "trend": "📈 稳定上升 — 广告、订阅、佣金模式越来越成熟",







            "key_employers": ["字节跳动(抖音/头条广告)", "腾讯(广告/游戏)", "百度(搜索广告)", "快手(电商/广告)", "小红书(商业化)", "B站(花火/广告)"]







        },







        "daily_work": [







            "设计和优化产品的变现模式和收入来源",







            "配置和管理广告库存、定价策略、促销活动",







            "监控核心变现指标(ARPU、付费率、LTV、ROI)",







            "A/B测试不同变现策略的效果",







            "与产品/工程团队合作开发新的商业化功能",







            "分析竞品的商业化策略并输出改进建议"







        ],







        "dev_path": [







            {"level": "L1 入门期 (0-1年)", "title": "商业化运营专员",







             "tasks": ["学习主流变现模式(广告/订阅/佣金/打赏)", "协助配置商业化产品和策略", "监控收入数据日报", "执行基础的A/B测试"],







             "skills": ["Excel高级功能", "基础SQL", "了解主流广告平台后台", "数据可视化"],







             "salary": "12-16K", "action": "系统学习一种变现模式的底层逻辑"},







            {"level": "L2 成长期 (1-3年)", "title": "商业化运营经理",







             "tasks": ["独立负责一条变现线的日常运营", "制定定价和促销策略", "优化变现漏斗各环节转化率", "对月度/季度收入目标负责"],







             "skills": ["SQL熟练", "A/B测试设计", "收入模型搭建", "跨部门推动力"],







             "salary": "20-30K", "action": "争取 owning 一条完整的收入线"},







            {"level": "L3 进阶期 (3-5年)", "title": "高级商业化运营",







             "tasks": ["负责多产品/多场景的变现策略", "搭建变现分析和预警体系", "探索新的收入增长点", "带领小型团队"],







             "skills": ["商业建模", "战略规划", "谈判能力", "团队管理"],







             "salary": "35-50K", "action": "从'赚今天的钱'到'规划明天的钱'"},







            {"level": "L4 专家期 (5年+)", "title": "商业化负责人/总监",







             "tasks": ["公司级商业化战略规划", "P&L(损益表)负责", "多团队协同(产品/销售/渠道)", "投资人关系和融资支持"],







             "skills": ["C-level沟通", "财务建模", "组织领导力", "行业前瞻判断"],







             "salary": "60-100K+ 股权", "action": "成为能讲清楚商业故事的人"}







        ],







        "competencies": ["数据敏感度和分析能力", "商业模式理解", "A/B测试和实验思维", "定价策略", "跨部门推动力", "结果导向"],







        "interview_qa": [







            {"q": "你如何理解商业化运营的核心？", "a": "核心是在用户体验和商业收益之间找到最优平衡点。好的商业化不是'榨干用户'，而是让愿意付费的人方便地付费，同时不让免费用户感到被打扰。具体来说就是三件事：①扩大漏斗顶层(更多用户触达变现点)；②提升每层转化率；③提高付费用户的LTV。"},







            {"q": "如果某个变现策略导致用户投诉增加，你怎么处理？", "a": "我会立即做三件事：①拉数据看影响面——多少用户受影响、投诉率涨了多少；②分层分析——是新用户还是老用户、是哪个场景触发；③快速迭代——要么调整策略阈值，要么优化展示方式。商业化不能只看短期收入，用户留存和口碑是长期收入的基石。"},







            {"q": "你如何设定一个合理的收入目标？", "a": "自下而上+自上而下结合。自下而上：基于历史数据(环比增速、季节性因素)、当前在做的优化项预期收益、新产品上线计划来估算。自上而下：根据公司整体目标和分配到这条线的比例。两者对不上时，找出gap的原因——是资源不足还是方法需要调整。"},







            {"q": "说说你最自豪的一个变现相关的项目？", "a": "(建议用STAR法则准备：Situation背景→Task你的任务→Action你做了什么→Result量化结果。重点突出：你发现了什么问题、用了什么方法、最终提升了多少收入/转化率。)"},







            {"q": "你对广告/付费墙/订阅这几种模式怎么看？", "a": "没有最好的模式，只有最适合产品阶段和用户群体的模式。早期产品适合免费+增值(Freemium)降低门槛；成熟产品可以尝试订阅锁定长期收入；流量型产品广告变现效率最高。关键是测试——用数据说话而不是凭感觉选择。"}







        ]







    },







    "品牌营销": {







        "aliases": ["品牌营销", "品牌策划", "品牌运营", "市场营销", "市场专员"],







        "salary_bj": {







            "junior": {"range": "10K-16K", "avg": "13K", "note": "0-2年，有创意作品集加分"},







            "mid": {"range": "18K-30K", "avg": "24K", "note": "3-5年，有成功品牌案例"},







            "senior": {"range": "30K-50K+", "avg": "40K", "note": "5年+，操盘过知名品牌"}







        },







        "market_analysis": {







            "demand": "🔥 高需求 — 新消费品牌崛起，传统品牌数字化转型",







            "supply": "⚠️ 供给充足但优质少 — 人多但懂品牌的少",







            "difficulty": "⭐⭐⭐ 中等 — 创意+执行+数据三者都要",







            "trend": "➡️ 稳定 — 品牌永远是企业的刚需",







            "key_employers": ["新消费品牌(完美日记/喜茶/泡泡玛特等)", "4A广告公司", "大厂市场部(字节/腾讯/阿里)", "品牌咨询公司"]







        },







        "daily_work": [







            "制定品牌定位和传播策略",







            "策划品牌营销Campaign(新品上市、节日营销等)",







            "管理媒介投放和KOL/KOC合作",







            "把控品牌视觉和调性的统一性",







            "监测品牌声量和舆情",







            "组织线下活动(发布会、快闪店等)"







        ],







        "dev_path": [







            {"level": "L1 入门期 (0-1年)", "title": "品牌营销专员/执行",







             "tasks": ["协助策划品牌活动", "对接供应商和执行方", "整理品牌素材库", "撰写基础传播文案"],







             "skills": ["文案写作", "PPT制作", "基础设计审美", "项目管理工具"],







             "salary": "10-13K", "action": "多看优秀案例，建立自己的案例库"},







            {"level": "L2 成长期 (1-3年)", "title": "品牌营销经理",







             "tasks": ["独立负责中小型Campaign", "管理KOL和媒介预算", "制定阶段性品牌传播计划", "跨部门协调产品/销售配合"],







             "skills": ["全案策划", "预算管理", "媒介策略", "创意brief撰写"],







             "salary": "18-26K", "action": "争取own一个完整campaign从策略到落地"},







            {"level": "L3 进阶期 (3-5年)", "title": "高级品牌经理/品牌负责人",







             "tasks": ["负责品牌年度规划和预算", "搭建品牌管理体系", "管理外部代理商", "对品牌资产(知名度/美誉度/忠诚度)负责"],







             "skills": ["品牌战略", "团队管理", "危机公关", "CEO级别汇报"],







             "salary": "30-45K", "action": "从'做活动'到'建品牌'的思维升级"},







            {"level": "L4 专家期 (5年+)", "title": "品牌总监/CMO",







             "tasks": ["公司品牌战略决策", "多品牌矩阵管理", "企业文化与雇主品牌", "董事会层面品牌叙事"],







             "skills": ["商业战略", "资本运作理解", "公众影响力", "组织变革"],







             "salary": "50-90K+ 股权", "action": "成为能为企业'讲故事'的战略伙伴"}







        ],







        "competencies": ["创意思维", "文案能力", "审美和品牌感", "项目管理", "媒介资源", "数据驱动的品牌评估"],







        "interview_qa": [







            {"q": "你认为什么是好品牌？", "a": "我认为好品牌有三个标准：①用户端——有清晰的认知和情感联结，用户愿意为品牌溢价买单；②商业端——能带来持续的竞争优势和利润；③社会端——传递正向价值观。比如XX品牌，它不只是卖产品，而是在倡导一种生活方式。"},







            {"q": "如何衡量品牌营销的效果？", "a": "品牌效果分短期和长期。短期看：曝光量、互动率、搜索指数变化、引流效果。长期看：品牌知名度( aided/unaided )、品牌好感度、考虑度、NPS。关键是建立基线数据，每次Campaign前后对比，而不是只看绝对值。"},







            {"q": "预算有限的情况下怎么做品牌？", "a": "聚焦！与其撒胡椒面不如集中火力：①选一个最核心的传播切入点；②用低成本高杠杆的方式(如社交话题、UGC激励、跨界联名)；③把每一分钱都用在能产生二次传播的地方。小预算也能做大声音，关键是有洞察的好创意。"}







        ]







    },







    "广告投放": {







        "aliases": ["广告投放", "投放优化师", "信息流投放", "SEM", "效果广告", "增长投放"],







        "salary_bj": {







            "junior": {"range": "10K-18K", "avg": "14K", "note": "0-2年，有实操经验即可"},







            "mid": {"range": "18K-35K", "avg": "26K", "note": "3-5年，有千万级账户经验"},







            "senior": {"range": "35K-60K+", "avg": "48K", "note": "5年+，多平台多行业经验"}







        },







        "market_analysis": {







            "demand": "🔥🔥🔥 极高 — 电商、教育、游戏、本地生活都需要投放",







            "supply": "⚠️ 缺熟手 — 会花钱且能花出ROI的人很少",







            "difficulty": "⭐⭐⭐ 入门易精通难 — 上手快但做出差异化难",







            "trend": "📈 快速增长 — AI赋能投放，但对策略要求更高",







            "key_employers": ["MCN机构", "电商代运营公司", "品牌方in-house", "广告代理公司", "游戏公司UA部门"]







        },







        "daily_work": [







            "在各广告平台(巨量引擎/千川/腾讯广告/磁力引擎等)创建和管理广告计划",







            "进行关键词/人群/素材的A/B测试",







            "监控实时消耗和转化数据，及时调整出价和定向",







            "分析投放数据产出日报/周报和优化建议",







            "与创意团队协作产出高转化素材",







            "管理日/周/月度预算分配"







        ],







        "dev_path": [







            {"level": "L1 入门期 (0-6个月)", "title": "投放助理/初级优化师",







             "tasks": ["学习广告平台后台操作", "协助搭建广告计划和素材上传", "数据表格维护", "竞品广告监控"],







             "skills": ["Excel", "至少一个广告平台操作", "基础数据敏感度", "细心"],







             "salary": "8-12K", "action": "考一个平台的认证(如巨量引擎认证)"},







            {"level": "L2 成长期 (6个月-2年)", "title": "广告投放优化师",







             "tasks": ["独立负责账户的日常优化", "制定投放策略和预算分配", "素材效果分析和创意方向反馈", "对ROI/CPA/CPS等核心指标负责"],







             "skills": ["多平台操作", "数据分析", "创意判断力", "沟通协调"],







             "salary": "12-22K", "action": "积累不同行业/不同目标的投放经验"},







            {"level": "L3 进阶期 (2-5年)", "title": "高级投放专家/投放主管",







             "tasks": ["管理多个账户和团队", "搭建投放SOP和方法论", "探索新平台和新玩法", "对大规模预算(百万级/月)的效率负责"],







             "skills": ["策略规划", "团队管理", "算法理解", "预算管控"],







             "salary": "25-40K", "action": "从'操作员'升级为'策略家'"},







            {"level": "L4 专家期 (5年+)", "title": "投放总监/增长负责人",







             "tasks": ["公司级增长策略", "全渠道投放组合优化", "团队建设和人才培养", "与CEO/CFO对齐增长目标"],







             "skills": ["商业全局观", "算法和产品理解", "领导力", "财务建模"],







             "salary": "45-80K+ 奖金", "action": "成为'花钱最能赚钱的人'"}







        ],







        "competencies": ["数据敏感度", "平台操作能力", "创意判断力", "预算管理", "测试思维", "抗压能力"],







        "interview_qa": [







            {"q": "你如何优化一个表现不好的广告计划？", "a": "我的排查顺序是：①先看数据——CTR低就改素材/标题，CVR低就检查落地页，CTR和CVR都正常就看成本是否超出出价；②再看定向——人群是不是太窄或太宽；③最后看出价策略——是不是竞争环境变了。每一步都会做A/B验证，不会一次性改太多变量。"},







            {"q": "你熟悉的广告平台有哪些？", "a": "(如实回答，然后补充)我最熟悉的是XX平台，但也了解XX和XX的基本逻辑。不同平台的差异在于：XX适合XX类型的投放，XX更适合XX。选平台要看产品属性和目标人群在哪里。"},







            {"q": "如何控制投放ROI？", "a": "三道防线：①事前——设好出价上限和日预算硬止损；②事中——每小时盯核心指标，异常立即调整；③事后——每日复盘归因，把钱花得好的渠道加码，差的砍掉或优化。ROI不是一天的事，但每天的小优化累积起来就是大提升。"}







        ]







    },







    "用户增长": {







        "aliases": ["用户增长", "增长运营", "增长黑客", "Growth Hacker", "增长经理"],







        "salary_bj": {







            "junior": {"range": "12K-20K", "avg": "16K", "note": "0-2年，有增长实验经验优先"},







            "mid": {"range": "20K-38K", "avg": "29K", "note": "3-5年，有从0到1增长案例"},







            "senior": {"range": "38K-60K+", "avg": "48K", "note": "5年+，带动过大盘增长"}







        },







        "market_analysis": {







            "demand": "🔥🔥🔥 极高 — 流量红利消失后，增长是所有公司的刚需",







            "supply": "⚠️ 很缺 — 真正懂增长的复合型人才极少",







            "difficulty": "⭐⭐⭐⭐⭐ 最难 — 需要技术+产品+运营+数据的综合能力",







            "trend": "🚀 快速上升 — AI时代增长方式在进化，机会很多",







            "key_employers": ["互联网大厂增长团队", "SaaS公司", "出海企业", "电商/零售", "金融科技"]







        },







        "daily_work": [







            "搭建和分析用户增长漏斗(AARRR模型)",







            "设计和执行增长实验(A/B Test、功能灰度等)",







            "分析用户行为数据，找到增长机会点",







            "策划裂变/ referral / 用户召回等增长活动",







            "与产品/工程/数据团队协作落地增长策略",







            "建立增长指标体系和监控仪表盘"







        ],







        "dev_path": [







            {"level": "L1 入门期 (0-1年)", "title": "增长运营专员",







             "tasks": ["学习AARRR模型和增长方法论", "协助执行增长实验和数据收集", "用户分群和画像分析基础", "竞品增长策略调研"],







             "skills": ["SQL基础", "Excel数据分析", "A/B测试概念", "用户行为分析工具(如神策/GrowingIO)"],







             "salary": "12-16K", "action": "读《增长黑客》《引爆点》建立框架认知"},







            {"level": "L2 成长期 (1-3年)", "title": "增长运营经理",







             "tasks": ["独立设计和运行增长实验", "负责一个增长指标(如注册转化/留存)", "提出产品功能改进建议并推动落地", "定期输出增长复盘报告"],







             "skills": ["SQL熟练", "统计分析", "实验设计", "产品 sense", "数据可视化"],







             "salary": "20-32K", "action": "积累'因为我的实验使X提升了Y%'的具体案例"},







            {"level": "L3 进阶期 (3-5年)", "title": "高级增长经理/增长负责人",







             "tasks": ["负责产品/业务线的整体增长策略", "搭建增长团队和SOP", "多指标协同优化(不只看单一指标)", "跨业务线增长最佳实践沉淀"],







             "skills": ["因果推断", "战略规划", "团队管理", "技术理解(能和工程师对话)"],







             "salary": "35-50K", "action": "从单点突破到系统工程"},







            {"level": "L4 专家期 (5年+)", "title": "增长总监/Head of Growth",







             "tasks": ["公司级增长战略", "新业务0到1增长操盘", "增长团队建设和文化塑造", "CEO/CFO的增长战略伙伴"],







             "skills": ["商业全局观", "技术架构理解", "组织设计", "投资人和董事会沟通"],







             "salary": "55-90K+ 股权", "action": "成为'公司增长引擎的设计者'"}







        ],







        "competencies": ["数据分析能力", "实验思维", "产品 sense", "技术理解力", "创造性解决问题", "结果导向"],







        "interview_qa": [







            {"q": "你如何理解用户增长？", "a": "增长不是'拉新'的代名词，而是用科学的方法系统地提升用户全生命周期价值。我用AARRR框架思考：获取(Acquisition)→激活(Activation)→留存(Retention)→变现(Revenue)→推荐(Referral)。每个环节都有优化的空间，关键是找到当前最大的杠杆点。"},







            {"q": "你做过最成功的增长实验是什么？", "a": "(STAR法则准备：背景是什么、你假设了什么、怎么设计的实验、对照组 vs 实验组的结果如何、统计显著性如何、后续怎么放量的。)"},







            {"q": "如果老板要求下个月新增用户翻倍，你会怎么做？", "a": "先拆解：翻倍意味着什么数字，当前的获客渠道和转化漏斗在哪。然后看三件事：①现有渠道能不能提效(优化转化率/提升预算)；②有没有未开发的渠道(新平台/新合作)；③产品内有没有自增长机制(裂变/referral/社交分享)。最后给出一个保守/基准/乐观三个方案供决策。"}







        ]







    }







}























def match_career_info(target_job):







    """根据目标岗位名称匹配职业数据库"""







    for key, info in CAREER_DB.items():







        if key in target_job or any(alias in target_job for alias in info["aliases"]):







            return key, info







    # 模糊匹配







    for key, info in CAREER_DB.items():







        for alias in info["aliases"]:







            if alias in target_job or target_job in alias:







                return key, info







    return None, None























def generate_optimized_resume(sections, target_job, career_key, supplements=None):







    """根据目标岗位生成优化后的简历"""







    matched_key, career_info = match_career_info(target_job)







    if not matched_key:







        matched_key = career_key







        career_info = CAREER_DB.get(career_key)







    







    competencies = career_info.get("competencies", []) if career_info else []







    







    optimized = {}







    







    # === 优化求职意向 ===







    if '求职意向' in sections:







        original = sections['求职意向']







        optimized['求职意向'] = f"""**目标岗位：{target_job}**







**期望城市：** 北京







**期望薪资：** 面议







**到岗时间：** 一周内















> 聚焦{matched_key or target_job}方向，具备{', '.join(competencies[:3])}等核心能力，







> 寻求能在实践中快速成长、为公司创造真实价值的平台。"""







    else:







        optimized['求职意向'] = f"""**目标岗位：{target_job}**







**期望城市：** 北京







**期望薪资：** 面议







**到岗时间：** 一周内"""







    







    # === 优化个人总结/自我评价 ===







    all_text = '\n'.join(sections.values())







    # 个人总结 - graceful degradation



    try:



        summary_result = generate_personal_summary(sections, target_job, matched_key, competencies, supplements)



        if summary_result.startswith('[AI生成失败'):



            optimized['个人总结'] = summary_result + '\n\n[说明：AI生成失败，你可以参考求职意向部分手动填写个人总结]'



        else:



            optimized['个人总结'] = summary_result



    except Exception as ex:



        optimized['个人总结'] = f'[生成失败: {str(ex)}]'







    







    # === 优化实习经历 ===







    if '实习经历' in sections:







        try:



            exp_result = optimize_experience(sections['实习经历'], target_job, competencies, supplements)



            optimized['实习经历'] = exp_result if not exp_result.startswith('[AI生成失败') else f'[部分内容生成失败] {exp_result}'



        except Exception as ex:



            optimized['实习经历'] = f'[生成失败: {str(ex)}]'







    







    # === 优化项目经验 ===







    if '项目经验' in sections:







        try:



            proj_result = optimize_experience(sections['项目经验'], target_job, competencies, supplements)



            optimized['项目经验'] = proj_result if not proj_result.startswith('[AI生成失败') else f'[部分内容生成失败] {proj_result}'



        except Exception as ex:



            optimized['项目经验'] = f'[生成失败: {str(ex)}]'







    







    # === 优化技能 ===







    if '技能证书' in sections:







        try:



            skills_result = optimize_skills(sections['技能证书'], target_job, competencies, supplements)



            optimized['技能证书'] = skills_result if not skills_result.startswith('[AI生成失败') else f'[部分内容生成失败] {skills_result}'



        except Exception as ex:



            optimized['技能证书'] = f'[生成失败: {str(ex)}]'







    







    # === 优化教育经历 ===







    if '教育经历' in sections:







        optimized['教育经历'] = sections['教育经历']







    







    # 原始内容保留







    optimized['_original_sections'] = sections







    optimized['_target_job'] = target_job







    optimized['_career_key'] = matched_key







    







    return optimized























def generate_personal_summary(sections, target_job, career_key, competencies, supplements=None):







    """用 AI 生成针对性的个人总结"""







    edu = sections.get('教育经历', '')







    exp = sections.get('实习经历', '')







    project = sections.get('项目经验', '')







    skills = sections.get('技能证书', '')







    eval_text = sections.get('自我评价', '')







    







    comp_str = '、'.join(competencies[:5]) if competencies else '运营、策划、数据分析'







    exp_desc = exp if exp else (project if project else '暂无实习/项目经历')







    







    # 将用户的补充内容加入 prompt



    supp_context = ''



    if supplements:



        supp_lines = []



        for kw, detail in supplements.items():



            if detail and detail.strip():



                supp_lines.append(f'用户补充的「{kw}」相关经历：{detail.strip()}')



        if supp_lines:



            supp_context = '\n用户补充信息：\n' + '\n'.join(supp_lines)







    prompt = f"你是一个专业的简历优化顾问。请根据以下简历内容，为一个应聘【{target_job}】岗位的应届生/实习生写一段专业的个人总结(150字以内)。要求：1) 第一人称，简洁有力 2) 突出与{target_job}岗位相关的经历和能力 3) 融入岗位关键词 4) 不要空洞套话，要具体信息点 5) 直接输出，不要加标题\n简历信息：教育：{edu[:200]} 实习/项目：{exp_desc[:300]} 技能：{skills[:200]} 自我评价：{eval_text[:200] if eval_text else '无'}{supp_context}\n直接输出："







    result = call_ai(prompt, max_tokens=500, temperature=0.7)







    return result























def optimize_experience(original_exp, target_job, competencies, supplements=None):



    """用 AI 优化实习/项目经历描述"""



    comp_str = '、'.join(competencies[:5]) if competencies else '运营、策划、数据分析'



    



    # 将用户的补充内容加入 prompt



    supp_context = ''



    if supplements:



        supp_lines = []



        for kw, detail in supplements.items():



            if detail and detail.strip():



                supp_lines.append(f'用户补充的经历（{kw}）：{detail.strip()}')



        if supp_lines:



            supp_context = '\n用户补充的相关经历：\n' + '\n'.join(supp_lines)



    



    prompt = f"你是一个资深HR。请将以下实习/项目经历用STAR法则优化重写，使其更专业、更有针对性。要求：1)每段经历先写小标题（格式：公司名/项目名，岗位/角色，核心能力）：然后换行写具体内容 2)STAR结构(情境-任务-行动-结果) 3)动词开头：负责、主导、推进、优化、搭建、分析等 4)量化成果，加具体数字 5)融入关键词：{comp_str} 6)每条2-4行 7)直接输出不加说明\n原始内容：{original_exp}{supp_context}\n优化后："



    result = call_ai(prompt, max_tokens=2000, temperature=0.7)
    result_text = result
    # 清理多余的section标题和重复空行
    lines = result_text.split('\n')
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if not prev_empty:
                cleaned_lines.append('')
                prev_empty = True
            continue
        prev_empty = False
        # 跳过多余的section标记（如【实习经历】【项目经验】【公司名/项目名】）
        if re.match(r'^【.+】$', stripped):
            continue
        # 移除行内多余空格，但保留结构
        line_clean = ' '.join(stripped.split())
        cleaned_lines.append(line_clean)
    # 移除开头和结尾的空行
    while cleaned_lines and not cleaned_lines[0]:
        cleaned_lines.pop(0)
    while cleaned_lines and not cleaned_lines[-1]:
        cleaned_lines.pop()
    return '\n'.join(cleaned_lines)
def optimize_skills(original_skills, target_job, competencies, supplements=None):







    """用 AI 优化技能板块"""







    comp_str = '、'.join(competencies[:6]) if competencies else '运营能力、数据分析、沟通协调、项目管理'







    prompt = f"你是一个资深HR。请优化以下技能描述，针对应聘【{target_job}】岗位。要求：1)优先展示与目标岗位最相关的技能 2)归类整理原始技能，保留有价值内容 3)适当补充该岗位常用技能 4)简洁分级列表形式 5)直接输出不加说明\n原始技能：{original_skills}\n目标岗位：{target_job}\n优化后："







    result = call_ai(prompt, max_tokens=600, temperature=0.7)







    return result























def generate_interview_answers(sections, target_job, career_key, supplements=None):



    """用 AI 生成个性化面试答案 - 结合用户实际经历"""



    exp = sections.get('实习经历', '') or sections.get('项目经验', '') or sections.get('校园经历', '') or sections.get('其他', '')



    skills = sections.get('技能证书', '')



    edu = sections.get('教育经历', '')



    



    # 将用户的补充内容加入



    supp_context = ''



    if supplements:



        supp_lines = []



        for kw, detail in supplements.items():



            if detail and detail.strip():



                supp_lines.append(f'用户补充的「{kw}」相关经历：{detail.strip()}')



        if supp_lines:



            supp_context = '\n用户补充的额外经历：\n' + '\n'.join(supp_lines)



    



    prompt = f"""你是一个资深HR面试官。请为应聘【{target_job}】岗位的候选人准备【7个】面试问题及【高度个性化】的答案。每个答案必须包含具体细节，字数不少于150字。

【核心要求】
1. 每个答案必须引用候选人的真实经历，提及具体的项目名称、公司名称、技能名称
2. 用STAR法则组织答案（情境-任务-行动-结果），让回答有说服力
3. 答案要像真人在面试时说的话，口语化、自然、有细节
4. 答案要150-180字，信息密度高
5. 问题类型：1个自我介绍、2个经历类、2个技能/优缺点类、2个职业规划/团队合作类

【输出格式】
Q1: 问题
A1: 答案
...

【候选人简历关键内容】
教育背景：{edu[:300]}
实习/项目经历：{exp[:800]}
技能证书：{skills[:400]}{supp_context}

【重要提醒】
- 必须引用简历中的真实信息（公司名、项目名、技能名）
- 不要编造不存在的经历
- 必须输出完整的7个问答，每个答案都要详细展开，不少于150字

请直接输出7个Q&A：
    """



    



    result = call_ai(prompt, max_tokens=4500, temperature=0.7)



    return result























# ============================================================







# 路由







# ============================================================















@app.route('/')







def index():







    return render_template('index.html')























@app.route('/api/upload', methods=['POST'])







def upload_resume():







    if 'resume' not in request.files:







        return jsonify({"error": "请上传PDF简历文件"}), 400







    







    file = request.files['resume']







    if not file.filename.lower().endswith('.pdf'):







        return jsonify({"error": "仅支持PDF格式"}), 400







    







    session_id = str(uuid.uuid4())[:8]







    filename = f"{session_id}_{file.filename}"







    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)







    file.save(filepath)







    







    # 提取文本







    text = extract_text_from_pdf(filepath)







    sections = parse_resume_sections(text)







    







    # 存储会话数据







    session_data = {







        "session_id": session_id,







        "filename": file.filename,







        "filepath": filepath,







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







        "filename": file.filename,







        "text_preview": text[:2000] + ("..." if len(text) > 2000 else ""),







        "sections": {k: (v[:500] + "..." if len(v) > 500 else v) for k, v in sections.items()},







        "section_count": len([v for v in sections.values() if len(v) > 20]),







        # AI job recommendations







        "job_recommendations": _get_ai_job_recommendations(text[:3000])



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







    # Save session first
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








































def _get_ai_job_recommendations(text):







    """用 AI 根据简历内容推荐适合的岗位"""







    prompt = f"你是一个资深职业规划师。请根据以下简历内容，推荐最合适的3个岗位，并给出职业发展路径建议。\n\n简历内容：\n{text}\n\n请按以下JSON格式输出(只输出JSON，不要任何其他文字)：\n{{'recommended_jobs':[{{'job':'岗位名','match_reason':'推荐理由(50字以内)','salary_range':'应届薪资范围','key_advice':'针对这个岗位的首要建议(50字以内)'}}],'career_path':'整体职业发展路径建议(80字以内)'}}\n\nJSON输出："







    







    result = call_ai(prompt, max_tokens=800, temperature=0.6)







    try:







        start = result.find('{')







        end = result.rfind('}') + 1







        if start != -1 and end > start:







            return json.loads(result[start:end])







    except:







        pass







    return {"recommended_jobs": [], "career_path": ""}























@app.route('/api/diagnose', methods=['POST'])







def diagnose():







    data = request.json







    session_id = data.get('session_id')







    target_job = data.get('target_job', '')







    







    session_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.json")







    if not os.path.exists(session_file):







        return jsonify({"error": "会话不存在，请重新上传简历"}), 400







    







    with open(session_file, 'r', encoding='utf-8') as f:







        session_data = json.load(f)







    







    sections = session_data.get('sections', {})







    diagnosis = diagnose_resume(sections, target_job)







    







    session_data['target_job'] = target_job







    session_data['diagnosis'] = diagnosis







    with open(session_file, 'w', encoding='utf-8') as f:







        json.dump(session_data, f, ensure_ascii=False, indent=2)







    







    return jsonify(diagnosis)























@app.route('/api/career', methods=['POST'])









def career_analysis():
    try:
        data = request.json
        session_id = data.get('session_id')
        target_job = data.get('target_job', '')
        session_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.json")
        if not os.path.exists(session_file):
            return jsonify({"error": "会话不存在"}), 400
        with open(session_file, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
            sections = session_data.get('sections', {})
            all_text = '\n'.join(f"【{k}】\n{sections[k]}" for k in sections if sections.get(k))
            matched_key, career_info = match_career_info(target_job)
            if not career_info:
                return jsonify({
                "error": f"暂无「{target_job}」的详细数据，支持的岗位：{', '.join(CAREER_DB.keys())}",
                "available_jobs": list(CAREER_DB.keys())
                }), 404
            # 用 AI 做个性化职业分析
            comp_str = '、'.join(career_info.get('competencies', [])[:6])
            ai_prompt = f"你是一个资深职业规划师。请根据以下简历内容，分析用户与「{target_job}」岗位的匹配度，并给出个性化职业建议。\n\n简历内容：\n{all_text[:2500]}\n\n目标岗位：{target_job}\n岗位核心能力要求：{comp_str}\n\n请按以下JSON格式输出（只输出JSON，不要其他文字）：\n{{\"match_score\":数字(0-100),\"match_advice\":\"一句话建议\",\"matched_keywords\":[\"关键词1\",\"关键词2\"],\"missing_keywords\":[\"缺失1\",\"缺失2\"],\"transferable_skills\":[\"可迁移技能1\",\"可迁移技能2\"],\"career_advice\":\"针对简历弱项的具体行动建议(100字以内)\"}}\nJSON："
            ai_result = call_ai(ai_prompt, max_tokens=600, temperature=0.3)
            ai_data = extract_json(ai_result) or {}
            # 关键词匹配
            job_kws = get_job_keywords(target_job)
            matched_kws = ai_data.get('matched_keywords', []) or [kw for kw in job_kws if kw in all_text]
            missing_kws = ai_data.get('missing_keywords', []) or [kw for kw in job_kws if kw not in all_text][:8]
            has_internship = '实习经历' in sections and len(sections['实习经历']) > 30
            has_project = '项目经验' in sections and len(sections['项目经验']) > 30
            match_score = ai_data.get('match_score', 50) or (len(matched_kws)*10 + (20 if has_internship else 0) + (15 if has_project else 0))
            match_score = max(10, min(95, match_score))
            if match_score >= 70:
                match_level = "🟢 较高匹配"
                base_advice = ai_data.get('match_advice', '简历与岗位比较对口')
            elif match_score >= 40:
                match_level = "🟡 中等匹配"
                base_advice = ai_data.get('match_advice', '有一定基础，需强化关键词')
            else:
                match_level = "🔴 匹配度较低"
                base_advice = ai_data.get('match_advice', '差距较大，需针对性补强')
            response = {
                "job_name": matched_key,
                "job_aliases": career_info["aliases"],
                "match_score": match_score,
                "match_level": match_level,
                "match_advice": base_advice,
                "matched_keywords": matched_kws[:6],
                "missing_keywords": missing_kws,
                "transferable_skills": ai_data.get('transferable_skills', []),
                "career_advice": ai_data.get('career_advice', ''),
                "has_internship": has_internship,
                "has_project": has_project,
                "salary": career_info["salary_bj"],
                "market": career_info["market_analysis"],
                "daily_work": career_info["daily_work"],
                "dev_path": career_info["dev_path"],
                "competencies": career_info["competencies"],
                "interview_qa": career_info.get("interview_qa", [])
                }
            session_data['career_info'] = response
            session_data['target_job'] = target_job
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
                return jsonify(response)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"职业分析失败: {str(e)[:80]}", "match_score": 30, "matched_keywords": [], "missing_keywords": [], "transferable_skills": [], "career_advice": "分析出错，请重试"})
@app.route('/api/optimize', methods=['POST'])
def optimize_resume():
    """优化简历（异步版本，AI调用超时180秒）"""
    data = request.json
    session_id = data.get('session_id')
    target_job = data.get('target_job', '')
    career_goal = data.get('career_goal', '')
    supplements = data.get('supplements', {})

    session_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.json")
    if not os.path.exists(session_file):
        return jsonify({"error": "会话不存在，请先上传简历"}), 400

    with open(session_file, 'r', encoding='utf-8') as f:
        session_data = json.load(f)

    sections = session_data.get('sections', {})
    matched_key, _ = match_career_info(target_job)

    # 异步执行简历优化（180秒超时）
    result_holder = [None]
    error_holder = [None]

    def _run_optimize():
        try:
            result_holder[0] = generate_optimized_resume(sections, target_job, matched_key, supplements)
        except Exception as e:
            error_holder[0] = str(e)

    t = threading.Thread(target=_run_optimize)
    t.start()
    t.join(timeout=180)

    if error_holder[0]:
        optimized = {'_error': error_holder[0], '_original_sections': sections, '_target_job': target_job, '_career_key': matched_key}
        optimized['岗位职责'] = f'**目标岗位：**{target_job}\n**简历评分：** 待优化\n**建议时间：** 一般需2-3天'
    elif t.is_alive():
        optimized = {'_timeout': True, '_original_sections': sections, '_target_job': target_job, '_career_key': matched_key}
        optimized['岗位职责'] = f'**目标岗位：**{target_job}\n**简历评分：** 优化中...\n**建议时间：** 请稍后刷新'
        optimized['个人总结'] = '[简历优化正在进行中，请稍后刷新页面查看结果]'
        optimized['求职意向'] = f'**目标岗位：** {target_job}'
    else:
        optimized = result_holder[0]
        if optimized is None:
            optimized = {'_error': '优化结果为空', '_original_sections': sections, '_target_job': target_job, '_career_key': matched_key}
            optimized['岗位职责'] = f'**目标岗位：**{target_job}\n**简历评分：** 待优化\n**建议时间：** 一般需2-3天'

    # 生成面试话术（同步，带超时）
    interview_result = None
    def _run_interview():
        try:
            nonlocal interview_result
            interview_result = generate_interview_answers(sections, target_job, matched_key, supplements=supplements)
            session_data['interview_ai'] = interview_result
        except:
            pass
    t_interview = threading.Thread(target=_run_interview)
    t_interview.start()
    t_interview.join(timeout=120)  # 等待最多120秒
    interview_ai = session_data.get('interview_ai')

    session_data['optimized_resume'] = optimized
    session_data['interview_ai'] = session_data.get('interview_ai')  # 同步AI生成的面试话术
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    return jsonify({
        **optimized,
        "interview_ai": session_data.get('interview_ai')
    })


def download_optimized(session_id):







    session_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.json")







    if not os.path.exists(session_file):







        return jsonify({"error": "文件不存在"}), 400







    







    with open(session_file, 'r', encoding='utf-8') as f:







        session_data = json.load(f)







    







    optimized = session_data.get('optimized_resume')







    if not optimized:







        return jsonify({"error": "请先生成优化简历"}), 400







    







    # 生成Markdown格式的优化简历







    md_content = format_resume_as_markdown(optimized, session_data)







    







    download_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_optimized_resume.md")







    with open(download_path, 'w', encoding='utf-8') as f:







        f.write(md_content)







    







    return send_file(download_path, as_attachment=True, 







                    download_name=f"优化简历_{session_data.get('target_job', 'resume')}.md",







                    mimetype='text/markdown'
                    )























def format_resume_as_markdown(optimized, session_data):







    """将优化后的简历格式化为Markdown"""







    target_job = optimized.get('_target_job', '目标岗位')







    lines = []







    lines.append(f"# 优化简历 - {target_job}")







    lines.append("")







    lines.append(f"> 📅 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")







    lines.append(f"> 🎯 目标岗位：{target_job}")







    lines.append("")







    lines.append("---")







    lines.append("")







    







    order = ['个人信息', '求职意向', '个人总结', '教育经历', '实习经历', '项目经验', '技能证书', '校园经历', '自我评价']







    







    written = set()







    for section in order:







        if section in optimized and section not in written:







            lines.append(optimized[section])







            lines.append("")







            lines.append("---")







            lines.append("")







            written.add(section)







    







    # 写入剩余板块







    for key, value in optimized.items():







        if key.startswith('_') or key in written:







            continue







        lines.append(f"### {key}")







        lines.append(value)







        lines.append("")







        written.add(key)







    







    # 附上面试Q&A







    career_key = optimized.get('_career_key')







    if career_key and career_key in CAREER_DB:







        # 优先使用AI生成的面试话术，如果没有则使用静态数据库
        qa_list = session_data.get('interview_ai') or CAREER_DB[career_key].get('interview_qa', [])







        if qa_list:







            lines.append("")







            lines.append("---")







            lines.append("")







            lines.append("## 🎤 面试常见问题 & 参考话术")







            lines.append("")







            for i, qa in enumerate(qa_list, 1):







                lines.append(f"### Q{i}: {qa['q']}")







                lines.append("")







                lines.append(f"**参考回答：** {qa['a']}")







                lines.append("")







    







    return '\n'.join(lines)























# Railway / Render 端口配置
PORT = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print("=" * 60)
    print("  简历优化助手 已启动!")
    print(f"  打开浏览器访问: http://127.0.0.1:{PORT}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)







