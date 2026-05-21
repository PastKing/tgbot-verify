# Gợi ý quy trình xác thực quân nhân SheerID cho ChatGPT

## 📋 Tổng quan

Quy trình xác thực quân nhân của ChatGPT khác với xác thực sinh viên/giáo viên thông thường, cần gọi thêm một API để thu thập trạng thái quân nhân trước, rồi mới gửi biểu mẫu thông tin cá nhân.

## 🔄 Quy trình xác thực

### Bước 1: Thu thập trạng thái quân nhân (collectMilitaryStatus)

Trước khi gửi biểu mẫu thông tin cá nhân, phải gọi API này để thiết lập trạng thái quân nhân.

**Thông tin yêu cầu**:
- **URL**: `https://services.sheerid.com/rest/v2/verification/{verificationId}/step/collectMilitaryStatus`
- **Phương thức**: `POST`
- **Tham số**:
```json
{
    "status": "VETERAN" // Tổng cộng 3 giá trị
}
```

**Ví dụ phản hồi**：
```json
{
    "verificationId": "{verification_id}",
    "currentStep": "collectInactiveMilitaryPersonalInfo",
    "errorIds": [],
    "segment": "military",
    "subSegment": "veteran",
    "locale": "en-US",
    "country": null,
    "created": 1766539517800,
    "updated": 1766540141435,
    "submissionUrl": "https://services.sheerid.com/rest/v2/verification/{verification_id}/step/collectInactiveMilitaryPersonalInfo",
    "instantMatchAttempts": 0
}
```

**Trường quan trọng**:
- `submissionUrl`: URL gửi của bước tiếp theo
- `currentStep`: bước hiện tại, nên chuyển thành `collectInactiveMilitaryPersonalInfo`

---

### Bước 2: Thu thập thông tin cá nhân của quân nhân không tại ngũ (collectInactiveMilitaryPersonalInfo)

Sử dụng `submissionUrl` trả về từ bước 1 để gửi thông tin cá nhân.

**Thông tin yêu cầu**:
 - **URL**: Lấy từ `submissionUrl` trong phản hồi của bước 1
     - Ví dụ: `https://services.sheerid.com/rest/v2/verification/{verificationId}/step/collectInactiveMilitaryPersonalInfo`
 - **Phương thức**: `POST`
 - **Tham số**:
```json
{
    "firstName": "name",
    "lastName": "name",
    "birthDate": "1939-12-01",
    "email": "your mail",
    "phoneNumber": "",
    "organization": {
        "id": 4070,
        "name": "Army"
    },
    "dischargeDate": "2025-05-29",
    "locale": "en-US",
    "country": "US",
    "metadata": {
        "marketConsentValue": false,
        "refererUrl": "",
        "verificationId": "",
        "flags": "{\"doc-upload-considerations\":\"default\",\"doc-upload-may24\":\"default\",\"doc-upload-redesign-use-legacy-message-keys\":false,\"docUpload-assertion-checklist\":\"default\",\"include-cvec-field-france-student\":\"not-labeled-optional\",\"org-search-overlay\":\"default\",\"org-selected-display\":\"default\"}",
        "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the <a target=\"_blank\" rel=\"noopener noreferrer\" class=\"sid-privacy-policy sid-link\" href=\"https://openai.com/policies/privacy-policy/\">privacy policy</a> of the business from which I am seeking a discount, and I understand that my personal information will be shared with SheerID as a processor/third-party service provider in order for SheerID to confirm my eligibility for a special offer. Contact OpenAI Support for further assistance at support@openai.com"
    }
}
```

**Giải thích các trường quan trọng**:
- `firstName`: tên
- `lastName`: họ
- `birthDate`: ngày sinh, định dạng `YYYY-MM-DD`
- `email`: địa chỉ email
- `phoneNumber`: số điện thoại (có thể để trống)
- `organization`: thông tin tổ chức quân đội (xem danh sách bên dưới)
- `dischargeDate`: ngày xuất ngũ, định dạng `YYYY-MM-DD`
- `locale`: vùng ngôn ngữ, mặc định `en-US`
- `country`: mã quốc gia, mặc định `US`
- `metadata`: dữ liệu metadata (bao gồm nội dung đồng ý chính sách quyền riêng tư, v.v.)

---

## 🎖️ Danh sách tổ chức quân đội (Organization)

Các tùy chọn tổ chức quân đội khả dụng:

```json
[
    {
        "id": 4070,
        "idExtended": "4070",
        "name": "Army",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4073,
        "idExtended": "4073",
        "name": "Air Force",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4072,
        "idExtended": "4072",
        "name": "Navy",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4071,
        "idExtended": "4071",
        "name": "Marine Corps",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4074,
        "idExtended": "4074",
        "name": "Coast Guard",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4544268,
        "idExtended": "4544268",
        "name": "Space Force",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    }
]
```

**Ánh xạ ID tổ chức**:
- `4070` - Army (Lục quân)
- `4073` - Air Force (Không quân)
- `4072` - Navy (Hải quân)
- `4071` - Marine Corps (Thủy quân lục chiến)
- `4074` - Coast Guard (Tuần duyên)
- `4544268` - Space Force (Lực lượng vũ trụ)

---

## 🔑 Điểm cần triển khai

1. **Phải thực hiện theo đúng thứ tự**: trước hết gọi `collectMilitaryStatus`, lấy `submissionUrl` rồi mới gọi `collectInactiveMilitaryPersonalInfo`
2. **Thông tin tổ chức**: trường `organization` cần có `id` và `name`, có thể chọn ngẫu nhiên từ danh sách trên hoặc cho người dùng chọn
3. **Định dạng ngày**: `birthDate` và `dischargeDate` phải dùng định dạng `YYYY-MM-DD`
4. **Metadata**: trường `submissionOptIn` trong `metadata` chứa nội dung đồng ý chính sách riêng tư, cần trích xuất hoặc tự dựng từ request gốc

---

## 📝 Tính năng cần triển khai

- [ ] Triển khai gọi API `collectMilitaryStatus`
- [ ] Triển khai gọi API `collectInactiveMilitaryPersonalInfo`
- [ ] Thêm logic chọn tổ chức quân đội
- [ ] Tạo thông tin cá nhân đúng yêu cầu (tên, ngày sinh, email, v.v.)
- [ ] Tạo ngày xuất ngũ (trong phạm vi hợp lý)
- [ ] Xử lý thông tin metadata (trích xuất hoặc dựng từ request gốc)
- [ ] Tích hợp vào hệ thống lệnh chính của bot (ví dụ `/verify6`)

