# Telegram bot tự động xác thực SheerID

![Stars](https://img.shields.io/github/stars/PastKing/tgbot-verify?style=social)
![Forks](https://img.shields.io/github/forks/PastKing/tgbot-verify?style=social)
![Issues](https://img.shields.io/github/issues/PastKing/tgbot-verify)
![License](https://img.shields.io/github/license/PastKing/tgbot-verify)

> 🤖 Telegram bot tự động hoàn tất xác thực SheerID cho sinh viên/giáo viên

[English](README_EN.md) | [Tiếng Việt](README.md)

---

## Giới thiệu

Dự án này là một Telegram bot viết bằng Python để tự động hóa quy trình xác thực SheerID cho nhiều dịch vụ. Bot có thể tạo thông tin ngẫu nhiên, sinh ảnh/tài liệu xác thực và gửi yêu cầu lên SheerID.

## Dịch vụ hỗ trợ

- `/verify` – Gemini One Pro
- `/verify2` – ChatGPT Teacher K12
- `/verify3` – Spotify Student
- `/verify4` – Bolt.new Teacher
- `/verify5` – YouTube Premium Student

## Tính năng chính

- Tự động tạo thông tin xác thực
- Tự động sinh PNG tài liệu
- Hỗ trợ MySQL và biến môi trường
- Kiểm soát đồng thời để ổn định hơn
- Có lệnh quản trị và hệ thống điểm

## Bắt đầu nhanh

```bash
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify
pip install -r requirements.txt
playwright install chromium
cp env.example .env
python bot.py
```

## Docker

```bash
docker-compose up -d
```

## Lệnh sử dụng

- `/start` – bắt đầu sử dụng
- `/about` – xem giới thiệu
- `/balance` – xem điểm
- `/qd` – điểm danh
- `/invite` – tạo liên kết mời
- `/use <mã>` – đổi điểm
- `/verify <link>` – xác thực Gemini One Pro
- `/verify2 <link>` – xác thực ChatGPT Teacher K12
- `/verify3 <link>` – xác thực Spotify Student
- `/verify4 <link>` – xác thực Bolt.new Teacher
- `/verify5 <link>` – xác thực YouTube Premium Student

## Cấu hình

- `BOT_TOKEN`: token Telegram bot
- `ADMIN_USER_ID`: ID quản trị viên
- `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`: cấu hình MySQL
- `CHANNEL_USERNAME`, `CHANNEL_URL`: cấu hình kênh

## Lưu ý

Nếu xác thực thất bại liên tục, hãy kiểm tra lại `programId` trong các file `config.py` của từng mô-đun.

## Liên hệ

- Telegram: [@pk_oa](https://t.me/pk_oa)
- Email: pastking69@gmail.com
- Issues: [GitHub Issues](https://github.com/PastKing/tgbot-verify/issues)

## Giấy phép

Dự án sử dụng giấy phép MIT.
