# Dùng image chính thức Python 3.11
FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các phụ thuộc hệ thống (Playwright cần)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    build-essential gcc pkg-config libcairo2-dev libpango1.0-dev libgdk-pixbuf-2.0-dev libffi-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Sao chép file phụ thuộc
COPY requirements.txt .

# Cài đặt phụ thuộc Python (không dùng cache)
RUN pip install --no-cache-dir -r requirements.txt

# Cài đặt trình duyệt Playwright
RUN playwright install chromium

# Sao chép file dự án (.dockerignore sẽ tự loại trừ cache)
COPY . .

# Dọn toàn bộ cache Python (đảm bảo dùng mã mới nhất)
RUN find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
RUN find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Không cho Python tạo bytecode (tránh vấn đề cache)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cấu hình MySQL (truyền qua docker-compose.yml hoặc dòng lệnh)
# Không hard-code ở đây, dùng biến môi trường

# Kiểm tra sức khỏe (kiểm tra tiến trình bot)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pgrep -f "python.*bot.py" || exit 1

# Khởi động bot
CMD ["python", "-u", "bot.py"]
