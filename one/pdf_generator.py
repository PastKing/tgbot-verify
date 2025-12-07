"""PDF 学生证生成模块"""
import random
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO


def generate_mit_id():
    """生成随机 MIT ID"""
    return f"9000{random.randint(10000, 99999)}"


def generate_pdf(first_name, last_name, school_id='1953'):
    """
    生成 MIT 学生成绩单 PDF
    
    Args:
        first_name: 名字
        last_name: 姓氏
        school_id: 学校 ID
    
    Returns:
        bytes: PDF 文件数据
    """
    mit_id = generate_mit_id()
    name = f"{first_name} {last_name}"
    date = datetime.now().strftime('%b %d, %Y')
    major = '6-3 (Computer Science)'
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Transcript</title>
    <style>
        @page {{ margin: 40px; }}
        body {{
            font-family: Helvetica, Arial, sans-serif;
            font-size: 12px;
            color: #333;
            line-height: 1.4;
        }}
        .header-table {{
            width: 100%;
            border-bottom: 2px solid #A31F34;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .mit-title {{
            font-family: "Times New Roman", serif;
            font-size: 24px;
            color: #000;
            margin: 0;
        }}
        .sub-title {{
            font-size: 10px;
            color: #8A8B8C;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .report-title {{
            text-align: right;
            font-weight: bold;
            color: #A31F34;
            font-size: 14px;
        }}
        .info-table {{
            width: 100%;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            margin-bottom: 20px;
        }}
        .info-table td {{
            padding: 8px;
            width: 50%;
        }}
        .label {{
            font-weight: bold;
            color: #555;
            margin-right: 10px;
        }}
        .term-header {{
            background-color: #8A8B8C;
            color: white;
            padding: 5px 10px;
            font-weight: bold;
            margin-top: 20px;
            font-size: 12px;
        }}
        .grade-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 11px;
            margin-bottom: 5px;
        }}
        .grade-table th {{
            text-align: left;
            border-bottom: 2px solid #ccc;
            padding: 5px;
            color: #444;
        }}
        .grade-table td {{
            padding: 5px;
            border-bottom: 1px solid #eee;
        }}
        .course-num {{ color: #A31F34; font-weight: bold; }}
        .footer {{
            position: fixed;
            bottom: 0px;
            left: 0px;
            right: 0px;
            font-size: 10px;
            color: #aaa;
            text-align: center;
            border-top: 1px solid #eee;
            padding-top: 10px;
        }}
    </style>
</head>
<body>
    <table class="header-table">
        <tr>
            <td valign="bottom">
                <div class="mit-title">Massachusetts Institute of Technology</div>
                <div class="sub-title">Office of the Registrar</div>
            </td>
            <td valign="bottom" align="right">
                <div class="report-title">UNOFFICIAL ACADEMIC RECORD<br>
                <span style="font-size:10px; color:#666; font-weight:normal;">Generated via WebSIS</span></div>
            </td>
        </tr>
    </table>

    <table class="info-table">
        <tr>
            <td><span class="label">Name:</span> {name}</td>
            <td><span class="label">MIT ID:</span> {mit_id}</td>
        </tr>
        <tr>
            <td><span class="label">Course:</span> {major}</td>
            <td><span class="label">Date:</span> {date}</td>
        </tr>
    </table>

    <div class="term-header">Fall 2024</div>
    <table class="grade-table">
        <thead>
            <tr>
                <th width="15%">Subject</th>
                <th width="60%">Title</th>
                <th width="10%">Units</th>
                <th width="15%">Grade</th>
            </tr>
        </thead>
        <tbody>
            <tr><td class="course-num">6.006</td><td>Introduction to Algorithms</td><td>12</td><td><b>A</b></td></tr>
            <tr><td class="course-num">6.009</td><td>Fundamentals of Programming</td><td>12</td><td><b>A</b></td></tr>
            <tr><td class="course-num">18.06</td><td>Linear Algebra</td><td>12</td><td><b>B+</b></td></tr>
            <tr><td class="course-num">8.01</td><td>Physics I</td><td>12</td><td><b>A-</b></td></tr>
        </tbody>
    </table>

    <div class="term-header">Spring 2025</div>
    <table class="grade-table">
        <thead>
            <tr>
                <th width="15%">Subject</th>
                <th width="60%">Title</th>
                <th width="10%">Units</th>
                <th width="15%">Grade</th>
            </tr>
        </thead>
        <tbody>
            <tr><td class="course-num">6.031</td><td>Software Construction</td><td>15</td><td><b>A</b></td></tr>
            <tr><td class="course-num">6.033</td><td>Computer System Engineering</td><td>12</td><td><b>A</b></td></tr>
            <tr><td class="course-num">14.01</td><td>Principles of Microeconomics</td><td>12</td><td><b>B</b></td></tr>
        </tbody>
    </table>

    <div class="term-header">Fall 2025 (In Progress)</div>
    <table class="grade-table">
        <thead>
            <tr>
                <th width="15%">Subject</th>
                <th width="60%">Title</th>
                <th width="10%">Units</th>
                <th width="15%">Status</th>
            </tr>
        </thead>
        <tbody>
            <tr><td class="course-num">6.036</td><td>Intro to Machine Learning</td><td>12</td><td>REG</td></tr>
            <tr><td class="course-num">6.046</td><td>Design & Analysis of Algorithms</td><td>12</td><td>REG</td></tr>
            <tr><td class="course-num">21G.101</td><td>Chinese I (Regular)</td><td>12</td><td>REG</td></tr>
        </tbody>
    </table>

    <div style="margin-top: 20px; text-align: right; border-top: 2px double #ccc; padding-top: 10px;">
        <strong>Cumulative GPA (5.0 Scale): <span style="color:#A31F34;">4.8</span></strong>
    </div>

    <div class="footer">
        This report is for the student's personal records. Generated on {date}.<br>
        Massachusetts Institute of Technology • 77 Massachusetts Avenue • Cambridge, MA 02139
    </div>
</body>
</html>
"""
    
    # 生成 PDF
    output = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=output)
    
    if pisa_status.err:
        raise Exception("PDF 生成失败")
    
    pdf_data = output.getvalue()
    output.close()
    
    return pdf_data

