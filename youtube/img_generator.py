"""Mô-đun tạo ảnh PNG thẻ sinh viên - Penn State LionPATH"""
import random
from datetime import datetime
from io import BytesIO
import base64


def generate_psu_id():
    """Tạo PSU ID ngẫu nhiên (9 chữ số)"""
    return f"9{random.randint(10000000, 99999999)}"


def generate_psu_email(first_name, last_name):
    """
    Tạo email PSU
    Định dạng: firstName.lastName + 3-4 chữ số @psu.edu
    """
    digit_count = random.choice([3, 4])
    digits = ''.join([str(random.randint(0, 9)) for _ in range(digit_count)])
    email = f"{first_name.lower()}.{last_name.lower()}{digits}@psu.edu"
    return email


def generate_html(first_name, last_name, school_id='2565'):
    """
    Tạo HTML Penn State LionPATH

    Args:
        first_name: Tên
        last_name: Họ
        school_id: ID trường

    Returns:
        str: Nội dung HTML
    """
    psu_id = generate_psu_id()
    name = f"{first_name} {last_name}"
    date = datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')

    # Chọn ngẫu nhiên ngành học
    majors = [
        'Computer Science (BS)',
        'Software Engineering (BS)',
        'Information Sciences and Technology (BS)',
        'Data Science (BS)',
        'Electrical Engineering (BS)',
        'Mechanical Engineering (BS)',
        'Business Administration (BS)',
        'Psychology (BA)'
    ]
    major = random.choice(majors)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LionPATH - Student Home</title>
    <style>
        :root {{
            --psu-blue: #1E407C; /* Penn State Nittany Navy */
            --psu-light-blue: #96BEE6;
            --bg-gray: #f4f4f4;
            --text-color: #333;
        }}

        body {{
            font-family: "Roboto", "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: #e0e0e0; /* Nền trình duyệt giả lập */
            margin: 0;
            padding: 20px;
            color: var(--text-color);
            display: flex;
            justify-content: center;
        }}

        /* Mô phỏng cửa sổ trình duyệt */
        .viewport {{
            width: 100%;
            max-width: 1100px;
            background-color: #fff;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            min-height: 800px;
            display: flex;
            flex-direction: column;
        }}

        /* Thanh điều hướng trên cùng LionPATH */
        .header {{
            background-color: var(--psu-blue);
            color: white;
            padding: 0 20px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        /* Mô phỏng logo PSU */
        .psu-logo {{
            font-family: "Georgia", serif;
            font-size: 20px;
            font-weight: bold;
            letter-spacing: 1px;
            border-right: 1px solid rgba(255,255,255,0.3);
            padding-right: 15px;
        }}

        .system-name {{
            font-size: 18px;
            font-weight: 300;
        }}

        .user-menu {{
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 20px;
        }}

        .nav-bar {{
            background-color: #f8f8f8;
            border-bottom: 1px solid #ddd;
            padding: 10px 20px;
            font-size: 13px;
            color: #666;
            display: flex;
            gap: 20px;
        }}
        .nav-item {{ cursor: pointer; }}
        .nav-item.active {{ color: var(--psu-blue); font-weight: bold; border-bottom: 2px solid var(--psu-blue); padding-bottom: 8px; }}

        /* Khu vực nội dung chính */
        .content {{
            padding: 30px;
            flex: 1;
        }}

        .page-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 20px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}

        .page-title {{
            font-size: 24px;
            color: var(--psu-blue);
            margin: 0;
        }}

        .term-selector {{
            background: #fff;
            border: 1px solid #ccc;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 14px;
            color: #333;
            font-weight: bold;
        }}

        /* Thẻ thông tin sinh viên */
        .student-card {{
            background: #fcfcfc;
            border: 1px solid #e0e0e0;
            padding: 15px;
            margin-bottom: 25px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            font-size: 13px;
        }}
        .info-label {{ color: #777; font-size: 11px; text-transform: uppercase; margin-bottom: 4px; }}
        .info-val {{ font-weight: bold; color: #333; font-size: 14px; }}
        .status-badge {{
            background-color: #e6fffa; color: #007a5e;
            padding: 4px 8px; border-radius: 4px; font-weight: bold; border: 1px solid #b2f5ea;
        }}

        /* Lịch học / Thời khoá biểu */
        .schedule-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}

        .schedule-table th {{
            text-align: left;
            padding: 12px;
            background-color: #f0f0f0;
            border-bottom: 2px solid #ccc;
            color: #555;
        }}

        .schedule-table td {{
            padding: 15px 12px;
            border-bottom: 1px solid #eee;
        }}

        .course-code {{ font-weight: bold; color: var(--psu-blue); }}
        .course-title {{ font-weight: 500; }}

        /* Tương thích in ấn */
        @media print {{
            body {{ background: white; padding: 0; }}
            .viewport {{ box-shadow: none; max-width: 100%; min-height: auto; }}
            .nav-bar {{ display: none; }}
            @page {{ margin: 1cm; size: landscape; }}
        }}
    </style>
</head>
<body>

<div class="viewport">
    <div class="header">
        <div class="brand">
            <div class="psu-logo">PennState</div>
            <div class="system-name">LionPATH</div>
        </div>
        <div class="user-menu">
            <span>Welcome, <strong>{name}</strong></span>
            <span>|</span>
            <span>Sign Out</span>
        </div>
    </div>

    <div class="nav-bar">
        <div class="nav-item">Student Home</div>
        <div class="nav-item active">My Class Schedule</div>
        <div class="nav-item">Academics</div>
        <div class="nav-item">Finances</div>
        <div class="nav-item">Campus Life</div>
    </div>

    <div class="content">
        <div class="page-header">
            <h1 class="page-title">My Class Schedule</h1>
            <div class="term-selector">
                Term: <strong>Fall 2025</strong> (Aug 25 - Dec 12)
            </div>
        </div>

        <div class="student-card">
            <div>
                <div class="info-label">Student Name</div>
                <div class="info-val">{name}</div>
            </div>
            <div>
                <div class="info-label">PSU ID</div>
                <div class="info-val">{psu_id}</div>
            </div>
            <div>
                <div class="info-label">Academic Program</div>
                <div class="info-val">{major}</div>
            </div>
            <div>
                <div class="info-label">Enrollment Status</div>
                <div class="status-badge">✅ Enrolled</div>
            </div>
        </div>

        <div style="margin-bottom: 10px; font-size: 12px; color: #666; text-align: right;">
            Data retrieved: <span>{date}</span>
        </div>

        <table class="schedule-table">
            <thead>
                <tr>
                    <th width="10%">Class Nbr</th>
                    <th width="15%">Course</th>
                    <th width="35%">Title</th>
                    <th width="20%">Days & Times</th>
                    <th width="10%">Room</th>
                    <th width="10%">Units</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>14920</td>
                    <td class="course-code">CMPSC 465</td>
                    <td class="course-title">Data Structures and Algorithms</td>
                    <td>MoWeFr 10:10AM - 11:00AM</td>
                    <td>Willard 062</td>
                    <td>3.00</td>
                </tr>
                <tr>
                    <td>18233</td>
                    <td class="course-code">MATH 230</td>
                    <td class="course-title">Calculus and Vector Analysis</td>
                    <td>TuTh 1:35PM - 2:50PM</td>
                    <td>Thomas 102</td>
                    <td>4.00</td>
                </tr>
                <tr>
                    <td>20491</td>
                    <td class="course-code">CMPSC 473</td>
                    <td class="course-title">Operating Systems Design</td>
                    <td>MoWe 2:30PM - 3:45PM</td>
                    <td>Westgate E201</td>
                    <td>3.00</td>
                </tr>
                <tr>
                    <td>11029</td>
                    <td class="course-code">ENGL 202C</td>
                    <td class="course-title">Technical Writing</td>
                    <td>Fr 1:25PM - 2:15PM</td>
                    <td>Boucke 304</td>
                    <td>3.00</td>
                </tr>
                <tr>
                    <td>15502</td>
                    <td class="course-code">STAT 318</td>
                    <td class="course-title">Elementary Probability</td>
                    <td>TuTh 9:05AM - 10:20AM</td>
                    <td>Osmond 112</td>
                    <td>3.00</td>
                </tr>
            </tbody>
        </table>

        <div style="margin-top: 50px; border-top: 1px solid #ddd; padding-top: 10px; font-size: 11px; color: #888; text-align: center;">
            &copy; 2025 The Pennsylvania State University. All rights reserved.<br>
            LionPATH is the student information system for Penn State.
        </div>
    </div>
</div>

</body>
</html>
"""

    return html


def generate_image(first_name, last_name, school_id='2565'):
    """
    Tạo ảnh chụp Penn State LionPATH (PNG)

    Args:
        first_name: Tên
        last_name: Họ
        school_id: ID trường

    Returns:
        bytes: Dữ liệu PNG
    """
    try:
        from playwright.sync_api import sync_playwright

        # Tạo HTML
        html_content = generate_html(first_name, last_name, school_id)

        # Dùng Playwright để chụp ảnh màn hình (thay cho Selenium)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1200, 'height': 900})
            page.set_content(html_content, wait_until='load')
            page.wait_for_timeout(500)  # Đợi style tải xong
            screenshot_bytes = page.screenshot(type='png', full_page=True)
            browser.close()

        return screenshot_bytes

    except ImportError:
        raise Exception("Cần cài đặt playwright: pip install playwright && playwright install chromium")
    except Exception as e:
        raise Exception(f"Tạo ảnh thất bại: {str(e)}")


if __name__ == '__main__':
    # Mã kiểm thử
    import sys
    import io

    # Sửa vấn đề mã hoá console trên Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("Kiểm thử tạo ảnh PSU...")

    first_name = "John"
    last_name = "Smith"

    print(f"Tên: {first_name} {last_name}")
    print(f"PSU ID: {generate_psu_id()}")
    print(f"Email: {generate_psu_email(first_name, last_name)}")

    try:
        img_data = generate_image(first_name, last_name)

        # Lưu ảnh kiểm thử
        with open('test_psu_card.png', 'wb') as f:
            f.write(img_data)

        print(f"✓ Tạo ảnh thành công! Kích thước: {len(img_data)} bytes")
        print("✓ Đã lưu thành test_psu_card.png")

    except Exception as e:
        print(f"✗ Lỗi: {e}")
