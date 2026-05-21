# Hướng dẫn triển khai

[English](DEPLOY_EN.md) | Tiếng Việt

Tài liệu này mô tả các cách triển khai SheerID bot trên Linux, macOS, Windows và Docker.

---

## Yêu cầu

- Python 3.11+
- MySQL 5.7+
- 512MB RAM trở lên
- Kết nối mạng ổn định
- Trình duyệt Chromium cho Playwright

---

## Triển khai nhanh bằng Docker Compose

```bash
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify
cp env.example .env
nano .env
docker-compose up -d
docker-compose logs -f
```

Dừng dịch vụ:

```bash
docker-compose down
```

---

## Triển khai Docker thủ công

```bash
docker build -t tgbot-verify:latest .
docker run -d \
  --name tgbot-verify \
  --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  tgbot-verify:latest
```

---

## Triển khai thủ công

### Linux / macOS

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-pip python3.11-venv mysql-server
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
python bot.py
```

### Windows

1. Cài Python 3.11+ và MySQL.
2. Tạo môi trường ảo bằng `py -3.11 -m venv .venv`.
3. Kích hoạt `.venv` và cài `requirements.txt`.
4. Chạy `playwright install chromium`.
5. Khởi động bot bằng `python bot.py`.

---

## Cấu hình

Tạo file `.env` từ `env.example` và điền các biến sau:

- `BOT_TOKEN`
- `ADMIN_USER_ID`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`
- `CHANNEL_USERNAME`
- `CHANNEL_URL`

---

## Xử lý sự cố

- **Bot token sai**: kiểm tra lại `BOT_TOKEN`.
- **Không kết nối được MySQL**: kiểm tra dịch vụ MySQL và thông tin đăng nhập.
- **Playwright lỗi**: chạy lại `playwright install chromium`.
- **Port bị chiếm**: kiểm tra cấu hình `docker-compose.yml`.
- **Thiếu bộ nhớ**: giảm mức song song hoặc tăng RAM.

---

## Cập nhật

```bash
git pull
docker-compose up -d --build
```

---

## Ghi chú

Một số mô-đun xác thực phụ thuộc vào `programId`. Nếu luồng xác thực thay đổi, hãy cập nhật các file `config.py` tương ứng.
