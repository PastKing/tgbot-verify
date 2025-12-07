# 使用Python 3.11官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（Playwright需要）
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

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖（不使用缓存）
RUN pip install --no-cache-dir -r requirements.txt

# 安装Playwright浏览器
RUN playwright install chromium

# 复制项目文件（.dockerignore会自动排除缓存）
COPY . .

# 清理所有Python缓存（确保使用最新代码）
RUN find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
RUN find . -type f -name "*.pyc" -delete 2>/dev/null || true

# 设置Python不生成字节码（避免缓存问题）
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# MySQL配置
ENV MYSQL_HOST=38.207.179.164
ENV MYSQL_PORT=3306
ENV MYSQL_USER=tgbot_verify
ENV MYSQL_PASSWORD=mYC5yTpwAMcLm3iT
ENV MYSQL_DATABASE=tgbot_verify

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import pymysql; pymysql.connect(host='38.207.179.164', user='tgbot_verify', password='mYC5yTpwAMcLm3iT', database='tgbot_verify').close()" || exit 1

# 启动并发版bot
CMD ["python", "-u", "bot_concurrent.py"]
