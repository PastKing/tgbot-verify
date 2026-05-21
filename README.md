# Telegram bot tự động xác thực SheerID

![Stars](https://img.shields.io/github/stars/PastKing/tgbot-verify?style=social)
![Forks](https://img.shields.io/github/forks/PastKing/tgbot-verify?style=social)
![Issues](https://img.shields.io/github/issues/PastKing/tgbot-verify)
![License](https://img.shields.io/github/license/PastKing/tgbot-verify)

> 🤖 Telegram bot tự động hoàn tất xác thực SheerID cho sinh viên/giáo viên
>
> Dựa trên mã nguồn cũ của GGBond từ [@auto_sheerid_bot](https://t.me/auto_sheerid_bot)

[English](README_EN.md) | [Tiếng Trung Phồn thể](README_TW.md) | Tiếng Việt

---

## 📋 Giới thiệu dự án

Telegram bot viết bằng Python, tự động hoàn tất xác thực danh tính sinh viên/giáo viên SheerID trên nhiều nền tảng. Bot tự tạo thông tin định danh, tạo tài liệu xác thực và gửi lên nền tảng SheerID, giúp đơn giản hóa đáng kể quy trình xác thực.

### 🎯 Dịch vụ xác thực được hỗ trợ

| Lệnh | Dịch vụ | Loại | Trạng thái |
|------|------|------|------|
| `/verify` | Gemini One Pro | Xác thực giáo viên | ✅ Hoàn chỉnh |
| `/verify2` | ChatGPT Teacher K12 | Xác thực giáo viên | ✅ Hoàn chỉnh |
| `/verify3` | Spotify Student | Xác thực sinh viên | ✅ Hoàn chỉnh |
| `/verify4` | Bolt.new Teacher | Xác thực giáo viên | ✅ Hoàn chỉnh |
| `/verify5` | YouTube Premium Student | Xác thực sinh viên | ⚠️ Đang phát triển |

> **⚠️ Cần đọc trước khi dùng**: `programId` của từng mô-đun có thể được cập nhật định kỳ, hãy kiểm tra và cập nhật file `config.py` tương ứng trước khi sử dụng, xem chi tiết ở phần "Cấu hình" bên dưới.

### ✨ Tính năng chính

- 🚀 **Quy trình tự động**: một chạm để tạo thông tin, tạo tài liệu và gửi xác thực
- 🎨 **Sinh tự động**: tự tạo ảnh PNG thẻ sinh viên/thẻ giáo viên
- 💰 **Hệ thống điểm**: nhiều cách nhận điểm như điểm danh, mời bạn, đổi mã
- 🔐 **An toàn, đáng tin cậy**: dùng MySQL và hỗ trợ cấu hình bằng biến môi trường
- ⚡ **Kiểm soát đồng thời**: quản lý số lượng yêu cầu song song để giữ ổn định
- 👥 **Quản trị**: hệ thống quản lý người dùng và điểm đầy đủ

---

## 🛠️ Công nghệ sử dụng

- **Ngôn ngữ**: Python 3.11+
- **Khung bot**: python-telegram-bot 20.0+
- **Cơ sở dữ liệu**: MySQL 5.7+
- **Tự động hóa trình duyệt**: Playwright
- **HTTP client**: httpx
- **Xử lý ảnh**: Pillow, reportlab, xhtml2pdf
- **Quản lý môi trường**: python-dotenv

---

## 🚀 Bắt đầu nhanh

### 1. Sao chép dự án

```bash
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify
```

### 2. Cài đặt phụ thuộc

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Cấu hình biến môi trường

Sao chép `env.example` thành `.env` và điền cấu hình:

```env
BOT_TOKEN=your_bot_token_here
CHANNEL_USERNAME=your_channel
CHANNEL_URL=https://t.me/your_channel
ADMIN_USER_ID=your_admin_id

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=tgbot_verify
```

### 4. Khởi động bot

```bash
python bot.py
```

---

## 🐳 Triển khai Docker

```bash
cp env.example .env
nano .env
docker-compose up -d
docker-compose logs -f
```

Xây dựng thủ công:

```bash
docker build -t tgbot-verify .
docker run -d --name tgbot-verify --env-file .env -v $(pwd)/logs:/app/logs tgbot-verify
```

---

## 📖 Hướng dẫn sử dụng

### Lệnh người dùng

```
/start              # Bắt đầu sử dụng (đăng ký)
/about              # Tìm hiểu tính năng của bot
/balance            # Xem số điểm hiện có
/qd                 # Điểm danh hằng ngày (+1 điểm)
/invite             # Tạo liên kết mời (+2 điểm/người)
/use <mã>           # Dùng mã để đổi điểm
/verify <link>      # Xác thực Gemini One Pro
/verify2 <link>     # Xác thực ChatGPT Teacher K12
/verify3 <link>     # Xác thực Spotify Student
/verify4 <link>     # Xác thực Bolt.new Teacher
/verify5 <link>     # Xác thực YouTube Premium Student
/help               # Xem trợ giúp
```

### Lệnh quản trị

```
/addbalance <user_id> <points>            # Cộng điểm cho người dùng
/block <user_id>                          # Chặn người dùng
/white <user_id>                          # Bỏ chặn
/blacklist                                # Xem danh sách đen
/genkey <mã> <điểm> [lần] [ngày]          # Tạo mã đổi điểm
/listkeys                                 # Xem danh sách mã
/broadcast <text>                         # Gửi thông báo hàng loạt
```

### Quy trình sử dụng

1. Mở trang xác thực của dịch vụ tương ứng để bắt đầu quy trình
2. Sao chép URL đầy đủ trong thanh địa chỉ có chứa `verificationId`
3. Gửi cho bot: `/verify3 https://services.sheerid.com/verify/xxx/?verificationId=yyy`
4. Chờ bot xử lý tự động, thường việc duyệt sẽ hoàn tất trong vài phút

---

## 📁 Cấu trúc dự án

```
tgbot-verify/
├── bot.py                  # Chương trình chính của bot
├── config.py               # Cấu hình toàn cục
├── database_mysql.py       # Quản lý cơ sở dữ liệu MySQL
├── env.example             # Mẫu biến môi trường
├── requirements.txt        # Phụ thuộc Python
├── Dockerfile              # Cấu hình Docker
├── docker-compose.yml      # Cấu hình Docker Compose
├── handlers/               # Bộ xử lý lệnh
│   ├── user_commands.py
│   ├── admin_commands.py
│   └── verify_commands.py
├── one/                    # Mô-đun Gemini One Pro
├── k12/                    # Mô-đun ChatGPT K12
├── spotify/                # Mô-đun Spotify Student
├── youtube/                # Mô-đun YouTube Premium
├── Boltnew/                # Mô-đun Bolt.new
├── military/               # Tài liệu xác thực quân nhân ChatGPT
└── utils/                  # Hàm tiện ích
    ├── messages.py
    ├── concurrency.py
    └── checks.py
```

---

## ⚙️ Cấu hình

### Biến môi trường

| Tên biến | Bắt buộc | Mô tả |
|--------|------|------|
| `BOT_TOKEN` | ✅ | Token bot Telegram |
| `ADMIN_USER_ID` | ✅ | Telegram ID của quản trị viên |
| `MYSQL_HOST` | ✅ | Địa chỉ máy chủ MySQL |
| `MYSQL_USER` | ✅ | Tên người dùng MySQL |
| `MYSQL_PASSWORD` | ✅ | Mật khẩu MySQL |
| `MYSQL_DATABASE` | ✅ | Tên cơ sở dữ liệu |
| `CHANNEL_USERNAME` | ❌ | Tên người dùng của kênh (mặc định pk_oa) |
| `CHANNEL_URL` | ❌ | Liên kết kênh |
| `MYSQL_PORT` | ❌ | Cổng MySQL (mặc định 3306) |

### Cập nhật programId

Nếu xác thực liên tục thất bại, thường là `programId` đã hết hạn. Các bước cập nhật:

1. Mở trang xác thực của dịch vụ tương ứng, mở công cụ nhà phát triển của trình duyệt (F12) → tab Network
2. Bắt đầu quy trình xác thực, tìm yêu cầu `https://services.sheerid.com/rest/v2/verification/`
3. Lấy `programId` từ yêu cầu và cập nhật file `config.py` của mô-đun tương ứng

Các file cần cập nhật: `one/config.py` | `k12/config.py` | `spotify/config.py` | `youtube/config.py` | `Boltnew/config.py`

### Cấu hình điểm (config.py)

```python
VERIFY_COST = 1        # Điểm trừ khi xác thực
CHECKIN_REWARD = 1     # Thưởng điểm danh
INVITE_REWARD = 2      # Thưởng mời bạn
REGISTER_REWARD = 1    # Thưởng đăng ký
```

---

## 🤝 Liên hệ và hợp tác

- 📢 **Kênh Telegram**: [@pk_oa](https://t.me/pk_oa)
- 📧 **Email**: pastking69@gmail.com
- 🐛 **Phản hồi lỗi**: [GitHub Issues](https://github.com/PastKing/tgbot-verify/issues)

Hoan nghênh hợp tác và trao đổi, nếu quan tâm hãy liên hệ qua các kênh trên.

---

## 🛠️ Phát triển tiếp

Hoan nghênh phát triển tiếp dựa trên dự án này, vui lòng tuân thủ các quy tắc sau:

- Giữ nguyên địa chỉ kho và thông tin tác giả
- Tuân thủ giấy phép mã nguồn mở MIT, dự án phái sinh cũng phải mở nguồn
- Sử dụng cá nhân là miễn phí; sử dụng thương mại hãy tự tối ưu và tự chịu trách nhiệm

---

## 📜 Giấy phép nguồn mở

Dự án này sử dụng giấy phép nguồn mở [MIT License](LICENSE).

---

## 🙏 Lời cảm ơn

- Cảm ơn GGBond của [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) vì nền tảng mã nguồn cũ
- Cảm ơn tất cả các nhà phát triển đã đóng góp cho dự án

---

## 📊 Thống kê dự án

[![Star History Chart](https://api.star-history.com/svg?repos=PastKing/tgbot-verify&type=Date)](https://star-history.com/#PastKing/tgbot-verify&Date)

---

<p align="center">
  <strong>⭐ Nếu dự án này hữu ích với bạn, hãy cho một Star để ủng hộ!</strong>
</p>

<p align="center">
  Được tạo với ❤️ bởi <a href="https://github.com/PastKing">PastKing</a>
</p>
