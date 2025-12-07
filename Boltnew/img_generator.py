"""PNG 教师证明生成模块 - Bolt.now / PSU"""
import random
from datetime import datetime


def generate_psu_id():
    """生成随机 PSU ID (9位数字)"""
    return f"9{random.randint(10000000, 99999999)}"


def generate_psu_email(first_name, last_name):
    """
    生成 PSU 邮箱
    格式: firstName.lastName + 3-4位数字 @psu.edu
    """
    digit_count = random.choice([3, 4])
    digits = ''.join([str(random.randint(0, 9)) for _ in range(digit_count)])
    email = f"{first_name.lower()}.{last_name.lower()}{digits}@psu.edu"
    return email


_browser_context = None
_page_pool = []


def _get_browser_context():
    """获取或创建浏览器上下文（单例模式）"""
    global _browser_context
    if _browser_context is None:
        try:
            from playwright.sync_api import sync_playwright
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--disable-extensions',
                ]
            )
            _browser_context = browser.new_context(
                viewport={'width': 1200, 'height': 1200},
                device_scale_factor=2,
            )
        except ImportError:
            raise Exception("需要安装 playwright: pip install playwright && playwright install chromium")
    return _browser_context


def _html_to_png(html_content: str, width: int = 1200, height: int = None) -> bytes:
    """将 HTML 转换为 PNG 截图（优化版：复用浏览器实例）"""
    try:
        context = _get_browser_context()
        page = context.new_page()

        try:
            # 直接设置 HTML 内容，使用 domcontentloaded 而非 networkidle（更快）
            page.set_content(html_content, wait_until='domcontentloaded')

            # 等待图片加载（如果有外部图片）
            page.wait_for_load_state('load', timeout=3000)

            # 自动计算高度
            if height is None:
                height = page.evaluate(
                    "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
                )

            page.set_viewport_size({'width': width, 'height': height})

            # 截图
            screenshot_bytes = page.screenshot(type='png', full_page=True)
            return screenshot_bytes
        finally:
            page.close()

    except Exception as e:
        raise Exception(f"生成图片失败: {str(e)}")


def generate_teacher_card_html(first_name: str, last_name: str, psu_id: str) -> str:
    """生成教师证件 HTML。"""
    timestamp = int(datetime.now().timestamp())
    name = f"{first_name} {last_name}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PSU Faculty id+ Card</title>
    <style>
        :root {{
            --psu-blue: #1E407C;
            --psu-light-blue: #96BEE6;
            --text-dark: #333;
        }}

        body {{
            background-color: #e0e0e0;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            flex-direction: column;
            gap: 20px;
        }}

        .card-container {{
            width: 320px;
            height: 504px;
            background-color: white;
            border-radius: 15px;
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .card-header {{
            width: 100%;
            height: 90px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 10px;
        }}

        .psu-brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .lion-shield {{
            width: 45px;
            height: 50px;
            background: var(--psu-blue);
            clip-path: polygon(0 0, 100% 0, 100% 75%, 50% 100%, 0 75%);
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .lion-shield::after {{
            content: "";
            width: 30px;
            height: 30px;
            background: white;
            mask: url('data:image/svg+xml;utf8,<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="40"/></svg>');
            -webkit-mask: url('data:image/svg+xml;utf8,<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="40"/></svg>');
        }}

        .psu-text {{
            display: flex;
            flex-direction: column;
        }}
        .psu-text span:first-child {{
            font-size: 20px;
            font-weight: 900;
            color: var(--psu-blue);
            text-transform: uppercase;
            line-height: 1;
        }}
        .psu-text span:last-child {{
            font-size: 20px;
            font-weight: 900;
            color: var(--psu-blue);
            text-transform: uppercase;
            line-height: 1;
        }}

        .photo-area {{
            width: 180px;
            height: 230px;
            background: #ddd;
            border: 2px solid var(--psu-blue);
            margin-top: 10px;
            overflow: hidden;
        }}
        
        .photo-area img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .info-area {{
            text-align: center;
            margin-top: 15px;
            flex-grow: 1;
        }}

        .name {{
            font-size: 26px;
            font-weight: bold;
            color: black;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}

        .id-number {{
            font-size: 16px;
            font-family: "Courier New", monospace;
            font-weight: bold;
            color: #555;
            letter-spacing: 1px;
        }}

        .footer-bar {{
            width: 100%;
            height: 50px;
            background-color: var(--psu-blue);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
            box-sizing: border-box;
        }}

        .role-text {{
            color: white;
            font-weight: bold;
            font-size: 18px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .id-plus-logo {{
            font-family: sans-serif;
            font-weight: bold;
            color: white;
            font-size: 24px;
            font-style: italic;
        }}
        .id-plus-logo span {{
            color: #96BEE6;
            font-style: normal;
        }}

        .hologram-overlay {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0) 40%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0) 60%);
            pointer-events: none;
            z-index: 10;
        }}

        @media print {{
            body {{ background: white; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            .card-container {{ box-shadow: none; border: 1px solid #ccc; }}
        }}
    </style>
</head>
<body>

<div class="card-container">
    <div class="hologram-overlay"></div>

    <div class="card-header">
        <div class="psu-brand">
            <div class="lion-shield"></div>
            <div class="psu-text">
                <span>Penn</span>
                <span>State</span>
            </div>
        </div>
    </div>

    <div class="photo-area">
        <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgwIiBoZWlnaHQ9IjIzMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTgwIiBoZWlnaHQ9IjIzMCIgZmlsbD0iI2RkZCIvPjxjaXJjbGUgY3g9IjkwIiBjeT0iNzAiIHI9IjMwIiBmaWxsPSIjYWFhIi8+PHBhdGggZD0iTTYwIDEzMCBROTAgMTEwIDEyMCAxMzAgTDEyMCAyMzAgTDYwIDIzMCBaIiBmaWxsPSIjYWFhIi8+PC9zdmc+" alt="Faculty Photo">
    </div>

    <div class="info-area">
        <div class="name">{name}</div>
        <div class="id-number">{psu_id}</div>
    </div>

    <div class="footer-bar">
        <div class="role-text">Faculty/Staff</div>
        <div class="id-plus-logo">id<span>+</span></div>
    </div>
</div>

</body>
</html>
"""


def generate_employment_letter_html(
    first_name: str, last_name: str, title: str, dept: str
) -> str:
    """生成教师在职证明 HTML。"""
    name = f"{first_name} {last_name}"
    now = datetime.now()
    date_str = now.strftime("%B %d, %Y")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PSU Employment Verification</title>
    <style>
        body {{
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
        }}

        .page {{
            width: 8.5in;
            min-height: 11in;
            background: white;
            padding: 1in;
            box-sizing: border-box;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            color: #333;
            position: relative;
        }}

        .header {{
            margin-bottom: 40px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 20px;
        }}

        .logo-area {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }}

        .psu-logo-mark {{
            width: 50px;
            height: 50px;
            background-color: #1E407C;
            mask: url('data:image/svg+xml;utf8,<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="45"/></svg>');
            -webkit-mask: url('data:image/svg+xml;utf8,<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="45"/></svg>');
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 28px;
            font-family: serif;
            margin-right: 15px;
        }}

        .org-name {{
            font-size: 18px;
            font-weight: bold;
            color: #1E407C;
            text-transform: uppercase;
        }}

        .hr-address {{
            font-size: 11px;
            color: #666;
            line-height: 1.4;
            text-align: right;
            position: absolute;
            top: 1in;
            right: 1in;
        }}

        .content {{
            font-size: 11pt;
            line-height: 1.6;
        }}

        .title {{
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            margin: 30px 0;
            text-transform: uppercase;
            text-decoration: underline;
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            font-size: 11pt;
        }}

        .data-table td {{
            padding: 8px 5px;
            border-bottom: 1px solid #eee;
        }}

        .data-label {{
            font-weight: bold;
            width: 40%;
            color: #555;
        }}

        .data-value {{
            font-weight: 600;
            color: #000;
        }}

        .footer {{
            position: absolute;
            bottom: 0.75in;
            left: 1in;
            right: 1in;
            font-size: 9px;
            color: #888;
            text-align: center;
            border-top: 1px solid #eee;
            padding-top: 10px;
        }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .page {{ box-shadow: none; margin: 0; width: 100%; height: auto; }}
        }}
    </style>
</head>
<body>

<div class="page">
    <div class="header">
        <div class="logo-area">
            <div class="psu-logo-mark">P</div>
            <div class="org-name">The Pennsylvania State University</div>
        </div>
        <div class="hr-address">
            <strong>Human Resources Shared Services</strong><br>
            The 331 Building<br>
            University Park, PA 16802<br>
            Phone: (814) 865-1473
        </div>
    </div>

    <div class="content">
        <div style="margin-bottom: 20px;">{date_str}</div>

        <div style="margin-bottom: 20px;">
            <strong>To Whom It May Concern:</strong>
        </div>

        <p>
            This letter is to verify the employment of the individual listed below with The Pennsylvania State University. This information is generated from the University's official Human Resources records system.
        </p>

        <div class="title">Certificate of Employment</div>

        <table class="data-table">
            <tr>
                <td class="data-label">Employee Name:</td>
                <td class="data-value">{name}</td>
            </tr>
            <tr>
                <td class="data-label">Job Profile / Title:</td>
                <td class="data-value">{title}</td>
            </tr>
            <tr>
                <td class="data-label">Primary Department:</td>
                <td class="data-value">{dept}</td>
            </tr>
            <tr>
                <td class="data-label">Employment Status:</td>
                <td class="data-value" style="color:green;">Active</td>
            </tr>
            <tr>
                <td class="data-label">Continuous Service Date:</td>
                <td class="data-value">August 15, 2018</td>
            </tr>
            <tr>
                <td class="data-label">Full-Time Equivalent (FTE):</td>
                <td class="data-value">100.0%</td>
            </tr>
            <tr>
                <td class="data-label">Pay Frequency:</td>
                <td class="data-value">Monthly</td>
            </tr>
        </table>

        <p>
            The employee listed above is currently an active member of the faculty/staff at Penn State. 
            Should you require further information regarding salary or detailed compensation, authorized requests may be submitted directly to PSU HR Shared Services.
        </p>

        <div style="margin-top: 50px;">
            Sincerely,
        </div>
        <div style="margin-top: 10px;">
            <strong>PSU Human Resources</strong><br>
            Records Management Team
        </div>
    </div>

    <div class="footer">
        Generated by Workday for The Pennsylvania State University | Report ID: WD-VER-99281 | {date_str}<br>
        This document is valid for 90 days from the date of issuance.
    </div>
</div>

</body>
</html>
"""


def _html_to_png_batch(html_list: list[tuple[str, int, int]]) -> list[bytes]:
    """
    批量并发生成多张 PNG（性能优化版）

    Args:
        html_list: [(html_content, width, height), ...]

    Returns:
        list[bytes]: PNG 数据列表
    """
    import asyncio
    from playwright.async_api import async_playwright

    async def render_single(html_content: str, width: int, height: int):
        """异步渲染单张图片"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--disable-extensions',
                ]
            )
            context = await browser.new_context(
                viewport={'width': width, 'height': height},
                device_scale_factor=2,
            )
            page = await context.new_page()

            try:
                await page.set_content(html_content, wait_until='domcontentloaded')
                await page.wait_for_load_state('load', timeout=3000)

                if height is None:
                    height = await page.evaluate(
                        "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
                    )
                    await page.set_viewport_size({'width': width, 'height': height})

                screenshot_bytes = await page.screenshot(type='png', full_page=True)
                return screenshot_bytes
            finally:
                await browser.close()

    async def render_all():
        """并发渲染所有图片"""
        tasks = [render_single(html, w, h) for html, w, h in html_list]
        return await asyncio.gather(*tasks)

    return asyncio.run(render_all())


def generate_images(first_name: str, last_name: str, school_id: str = '2565'):
    """
    生成两张 PNG：教师卡片 + 在职证明（并发优化版）

    Args:
        first_name: 名
        last_name: 姓
        school_id: 学校 ID（保留接口一致）

    Returns:
        list[dict]: [{"file_name": str, "data": bytes}]
    """
    psu_id = generate_psu_id()
    titles = [
        "Associate Professor",
        "Assistant Professor",
        "Teaching Professor",
        "Instructor",
        "Adjunct Faculty",
    ]
    departments = [
        "College of Engineering",
        "Department of Computer Science and Engineering",
        "Eberly College of Science",
        "College of Education",
        "Smeal College of Business",
    ]
    title = random.choice(titles)
    dept = random.choice(departments)

    card_html = generate_teacher_card_html(first_name, last_name, psu_id)
    letter_html = generate_employment_letter_html(first_name, last_name, title, dept)

    # 并发生成两张图片
    html_list = [
        (card_html, 700, 1100),
        (letter_html, 1300, 1600),
    ]

    results = _html_to_png_batch(html_list)
    card_png, letter_png = results

    return [
        {"file_name": "teacher_id.png", "data": card_png},
        {"file_name": "employment_letter.png", "data": letter_png},
    ]


if __name__ == '__main__':
    # 简单测试
    assets = generate_images("John", "Smith")
    for asset in assets:
        with open(asset["file_name"], "wb") as f:
            f.write(asset["data"])
        print(f"Generated {asset['file_name']} ({len(asset['data'])} bytes)")
