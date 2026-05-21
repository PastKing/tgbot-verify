"""Tạo tài liệu chứng minh giáo viên (PDF + PNG)"""
import random
from datetime import datetime
from io import BytesIO
from pathlib import Path

from xhtml2pdf import pisa


def _render_template(first_name: str, last_name: str) -> str:
    """Đọc mẫu, thay tên/mã nhân viên/ngày và mở rộng biến CSS."""
    full_name = f"{first_name} {last_name}"
    employee_id = random.randint(1000000, 9999999)
    current_date = datetime.now().strftime("%m/%d/%Y %I:%M %p")

    template_path = Path(__file__).parent / "card-temp.html"
    html = template_path.read_text(encoding="utf-8")

    # Mở rộng biến CSS để tương thích với xhtml2pdf
    color_map = {
        "var(--primary-blue)": "#0056b3",
        "var(--border-gray)": "#dee2e6",
        "var(--bg-gray)": "#f8f9fa",
    }
    for placeholder, color in color_map.items():
        html = html.replace(placeholder, color)

    # Thay tên mẫu / mã nhân viên / ngày (mẫu có hai chỗ tên + span)
    html = html.replace("Sarah J. Connor", full_name)
    html = html.replace("E-9928104", f"E-{employee_id}")
    html = html.replace('id="currentDate"></span>', f'id="currentDate">{current_date}</span>')

    return html


def generate_teacher_pdf(first_name: str, last_name: str) -> bytes:
    """Tạo byte PDF tài liệu chứng minh giáo viên."""
    html = _render_template(first_name, last_name)

    output = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=output, encoding="utf-8")
    if pisa_status.err:
        raise Exception("Tạo PDF thất bại")

    pdf_data = output.getvalue()
    output.close()
    return pdf_data


def generate_teacher_png(first_name: str, last_name: str) -> bytes:
    """Dùng Playwright chụp màn hình để tạo PNG (cần cài playwright + chromium)."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "Cần cài playwright, hãy chạy `pip install playwright` rồi `playwright install chromium`"
        ) from exc

    html = _render_template(first_name, last_name)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1200, "height": 1000})
        page.set_content(html, wait_until="load")
        page.wait_for_timeout(500)  # Chờ kiểu dáng ổn định
        card = page.locator(".browser-mockup")
        png_bytes = card.screenshot(type="png")
        browser.close()

    return png_bytes


# Tương thích với cách gọi cũ: mặc định tạo PDF
def generate_teacher_image(first_name: str, last_name: str) -> bytes:
    return generate_teacher_pdf(first_name, last_name)
