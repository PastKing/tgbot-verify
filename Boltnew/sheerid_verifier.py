"""Mô-đun xác thực SheerID giáo viên cho Bolt.new"""
import logging
import random
import re
from typing import Dict, Optional, Tuple
from urllib.parse import parse_qs, urlparse

import httpx

from . import config
from .img_generator import generate_images, generate_psu_email
from .name_generator import NameGenerator, generate_birth_date

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
)
logger = logging.getLogger(__name__)


class SheerIDVerifier:
    """Trình xác thực giáo viên SheerID."""

    def __init__(self, install_page_url: str, verification_id: Optional[str] = None):
        self.install_page_url = self.normalize_url(install_page_url)
        self.verification_id = verification_id or self.parse_verification_id(self.install_page_url)
        self.external_user_id = self.parse_external_user_id(self.install_page_url)
        self.device_fingerprint = self._generate_device_fingerprint()
        self.http_client = httpx.Client(timeout=30.0)

    def __del__(self):
        if hasattr(self, "http_client"):
            self.http_client.close()

    @staticmethod
    def _generate_device_fingerprint() -> str:
        chars = "0123456789abcdef"
        return "".join(random.choice(chars) for _ in range(32))

    @staticmethod
    def normalize_url(url: str) -> str:
        """Chuẩn hóa URL đầu vào nhưng giữ nguyên tham số gốc."""
        return url.strip()

    @staticmethod
    def parse_verification_id(url: str) -> Optional[str]:
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def parse_external_user_id(url: str) -> Optional[str]:
        parsed = urlparse(url)
        query_external_user_id = parse_qs(parsed.query).get("externalUserId")
        if query_external_user_id:
            return query_external_user_id[0]

        match = re.search(r"externalUserId=([^&?#/]+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def create_verification(self) -> str:
        """Tạo `verificationId` mới từ `installPageUrl`."""
        body = {
            "programId": config.PROGRAM_ID,
            "installPageUrl": self.install_page_url,
        }
        data, status = self._sheerid_request(
            "POST", f"{config.MY_SHEERID_URL}/rest/v2/verification/", body
        )
        if status != 200 or not isinstance(data, dict) or not data.get("verificationId"):
            raise Exception(f"Tạo verification thất bại (mã trạng thái {status}): {data}")

        self.verification_id = data["verificationId"]
        logger.info(f"✅ Đã lấy verificationId: {self.verification_id}")
        return self.verification_id

    def _sheerid_request(
        self, method: str, url: str, body: Optional[Dict] = None
    ) -> Tuple[Dict, int]:
        """Gửi yêu cầu đến API SheerID."""
        headers = {"Content-Type": "application/json"}

        try:
            response = self.http_client.request(
                method=method, url=url, json=body, headers=headers
            )
            try:
                data = response.json()
            except Exception:
                data = response.text
            return data, response.status_code
        except Exception as e:
            logger.error(f"Yêu cầu SheerID thất bại: {e}")
            raise

    def _upload_to_s3(self, upload_url: str, img_data: bytes) -> bool:
        """Tải PNG lên S3."""
        try:
            headers = {"Content-Type": "image/png"}
            response = self.http_client.put(
                upload_url, content=img_data, headers=headers, timeout=60.0
            )
            return 200 <= response.status_code < 300
        except Exception as e:
            logger.error(f"Tải lên S3 thất bại: {e}")
            return False

    def verify(
        self,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        birth_date: str = None,
        school_id: str = None,
    ) -> Dict:
        """Thực thi quy trình xác thực giáo viên."""
        try:
            current_step = "initial"

            if not first_name or not last_name:
                name = NameGenerator.generate()
                first_name = name["first_name"]
                last_name = name["last_name"]

            school_id = school_id or config.DEFAULT_SCHOOL_ID
            school = config.SCHOOLS[school_id]

            if not email:
                email = generate_psu_email(first_name, last_name)
            if not birth_date:
                birth_date = generate_birth_date()
            if not self.external_user_id:
                self.external_user_id = str(random.randint(1000000, 9999999))

            if not self.verification_id:
                logger.info("Đang xin verificationId mới...")
                self.create_verification()

            logger.info(f"Thông tin giáo viên: {first_name} {last_name}")
            logger.info(f"Email: {email}")
            logger.info(f"Trường: {school['name']}")
            logger.info(f"Ngày sinh: {birth_date}")
            logger.info(f"Verification ID: {self.verification_id}")

            logger.info("Bước 1/5: Tạo tài liệu PNG giáo viên...")
            assets = generate_images(first_name, last_name, school_id)
            for asset in assets:
                logger.info(
                    f"  - {asset['file_name']} ({len(asset['data']) / 1024:.2f}KB)"
                )

            logger.info("Bước 2/5: Gửi thông tin giáo viên...")
            step2_body = {
                "firstName": first_name,
                "lastName": last_name,
                "birthDate": "",
                "email": email,
                "phoneNumber": "",
                "organization": {
                    "id": int(school_id),
                    "idExtended": school["idExtended"],
                    "name": school["name"],
                },
                "deviceFingerprintHash": self.device_fingerprint,
                "externalUserId": self.external_user_id,
                "locale": "en-US",
                "metadata": {
                    "marketConsentValue": True,
                    "refererUrl": self.install_page_url,
                    "externalUserId": self.external_user_id,
                    "flags": '{"doc-upload-considerations":"default","doc-upload-may24":"default","doc-upload-redesign-use-legacy-message-keys":false,"docUpload-assertion-checklist":"default","include-cvec-field-france-student":"not-labeled-optional","org-search-overlay":"default","org-selected-display":"default"}',
                    "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount",
                },
            }

            step2_data, step2_status = self._sheerid_request(
                "POST",
                f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectTeacherPersonalInfo",
                step2_body,
            )

            if step2_status != 200:
                raise Exception(f"Bước 2 thất bại (mã trạng thái {step2_status}): {step2_data}")
            if isinstance(step2_data, dict) and step2_data.get("currentStep") == "error":
                error_msg = ", ".join(step2_data.get("errorIds", ["Unknown error"]))
                raise Exception(f"Bước 2 lỗi: {error_msg}")

            current_step = (
                step2_data.get("currentStep", current_step)
                if isinstance(step2_data, dict)
                else current_step
            )
            logger.info(f"✅ Bước 2 hoàn tất: {current_step}")

            if current_step in ["sso", "collectTeacherPersonalInfo"]:
                logger.info("Bước 3/5: Bỏ qua xác thực SSO...")
                step3_data, _ = self._sheerid_request(
                    "DELETE",
                    f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/sso",
                )
                current_step = (
                    step3_data.get("currentStep", current_step)
                    if isinstance(step3_data, dict)
                    else current_step
                )
                logger.info(f"✅ Bước 3 hoàn tất: {current_step}")

            logger.info("Bước 4/5: Yêu cầu đường dẫn tải lên...")
            step4_body = {
                "files": [
                    {
                        "fileName": asset["file_name"],
                        "mimeType": "image/png",
                        "fileSize": len(asset["data"]),
                    }
                    for asset in assets
                ]
            }
            step4_data, step4_status = self._sheerid_request(
                "POST",
                f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload",
                step4_body,
            )
            if step4_status != 200 or not isinstance(step4_data, dict) or not step4_data.get("documents"):
                raise Exception(f"Không lấy được URL tải lên: {step4_data}")

            documents = step4_data["documents"]
            if len(documents) != len(assets):
                raise Exception("Số tác vụ tải lên không khớp với số tệp")

            for doc, asset in zip(documents, assets):
                upload_url = doc.get("uploadUrl")
                if not upload_url:
                    raise Exception("Thiếu URL tải lên")
                if not self._upload_to_s3(upload_url, asset["data"]):
                    raise Exception(f"Tải lên S3 thất bại: {asset['file_name']}")
                logger.info(f"✅ Đã tải lên {asset['file_name']}")

            step6_data, _ = self._sheerid_request(
                "POST",
                f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload",
            )
            logger.info(
                f"✅ Gửi tài liệu hoàn tất: {getattr(step6_data, 'get', lambda k, d=None: d)('currentStep')}"
            )

            final_status, _ = self._sheerid_request(
                "GET",
                f"{config.MY_SHEERID_URL}/rest/v2/verification/{self.verification_id}",
            )
            reward_code = None
            if isinstance(final_status, dict):
                reward_code = final_status.get("rewardCode") or final_status.get("rewardData", {}).get("rewardCode")

            pending = True
            redirect_url = None
            if isinstance(final_status, dict):
                pending = final_status.get("currentStep") != "success"
                redirect_url = final_status.get("redirectUrl")

            return {
                "success": True,
                "pending": pending,
                "message": "Tài liệu đã được gửi, đang chờ duyệt" if pending else "Xác thực thành công",
                "verification_id": self.verification_id,
                "redirect_url": redirect_url,
                "reward_code": reward_code,
                "status": final_status,
            }

        except Exception as e:
            logger.error(f"❌ Xác thực thất bại: {e}")
            return {"success": False, "message": str(e), "verification_id": self.verification_id}


def main():
    """Hàm chính - giao diện dòng lệnh."""
    import sys

    print("=" * 60)
    print("Công cụ xác thực danh tính giáo viên SheerID (bản Python)")
    print("=" * 60)
    print()

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Vui lòng nhập URL xác thực SheerID (có externalUserId): ").strip()

    if not url:
        print("❌ Lỗi: chưa cung cấp URL")
        sys.exit(1)

    verification_id = SheerIDVerifier.parse_verification_id(url)
    verifier = SheerIDVerifier(url, verification_id=verification_id)

    print(f"👉 Đường dẫn sử dụng: {verifier.install_page_url}")
    if verifier.verification_id:
        print(f"Đã phân tích được verificationId: {verifier.verification_id}")
    if verifier.external_user_id:
        print(f"externalUserId: {verifier.external_user_id}")
    print()

    result = verifier.verify()

    print()
    print("=" * 60)
    print("Kết quả xác thực:")
    print("=" * 60)
    print(f"Trạng thái: {'✅ Thành công' if result['success'] else '❌ Thất bại'}")
    print(f"Thông báo: {result['message']}")
    if result.get("reward_code"):
        print(f"Mã ưu đãi: {result['reward_code']}")
    if result.get("redirect_url"):
        print(f"URL chuyển hướng: {result['redirect_url']}")
    print("=" * 60)

    return 0 if result["success"] else 1


if __name__ == "__main__":
    exit(main())
