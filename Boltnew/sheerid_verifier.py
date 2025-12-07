"""SheerID 教师验证主程序（Bolt.now）"""
import re
import random
import logging
import httpx
from typing import Dict, Optional, Tuple

from . import config
from .name_generator import NameGenerator, generate_birth_date
from .img_generator import generate_images, generate_psu_email

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
)
logger = logging.getLogger(__name__)


class SheerIDVerifier:
    """SheerID 教师身份验证器"""

    def __init__(self, install_page_url: str, verification_id: Optional[str] = None):
        self.install_page_url = self.normalize_url(install_page_url)
        self.verification_id = verification_id
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
        """规范化 URL（保留原样，兼容现有接口）"""
        return url

    @staticmethod
    def parse_verification_id(url: str) -> Optional[str]:
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def parse_external_user_id(url: str) -> Optional[str]:
        match = re.search(r"externalUserId=([^&]+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def create_verification(self) -> str:
        """通过 installPageUrl 申请新的 verificationId"""
        body = {
            "programId": config.PROGRAM_ID,
            "installPageUrl": self.install_page_url,
        }
        data, status = self._sheerid_request(
            "POST", f"{config.MY_SHEERID_URL}/rest/v2/verification/", body
        )
        if status != 200 or not isinstance(data, dict) or not data.get("verificationId"):
            raise Exception(f"创建 verification 失败 (状态码 {status}): {data}")

        self.verification_id = data["verificationId"]
        logger.info(f"✅ 获取 verificationId: {self.verification_id}")
        return self.verification_id

    def verify_hcaptcha(self, token: str) -> bool:
        if not config.HCAPTCHA_SECRET or not token:
            return not config.HCAPTCHA_SECRET
        try:
            response = self.http_client.post(
                "https://hcaptcha.com/siteverify",
                data={"response": token, "secret": config.HCAPTCHA_SECRET},
            )
            result = response.json()
            return result.get("success", False)
        except Exception as e:
            logger.error(f"hCaptcha 验证失败: {e}")
            return False

    def verify_turnstile(self, token: str) -> bool:
        if not config.TURNSTILE_SECRET or not token:
            return not config.TURNSTILE_SECRET
        try:
            response = self.http_client.post(
                "https://challenges.cloudflare.com/turnstile/v0/siteverify",
                data={"secret": config.TURNSTILE_SECRET, "response": token},
            )
            result = response.json()
            return result.get("success", False)
        except Exception as e:
            logger.error(f"Turnstile 验证失败: {e}")
            return False

    def _sheerid_request(
        self, method: str, url: str, body: Optional[Dict] = None
    ) -> Tuple[Dict, int]:
        """发送 SheerID API 请求"""
        headers = {
            "Content-Type": "application/json",
        }

        response = self.http_client.request(
            method=method, url=url, json=body, headers=headers
        )
        try:
            data = response.json()
        except Exception:
            data = response.text
        return data, response.status_code

    def _upload_to_s3(self, upload_url: str, img_data: bytes) -> bool:
        """上传 PNG 到 S3"""
        try:
            headers = {"Content-Type": "image/png"}
            response = self.http_client.put(
                upload_url, content=img_data, headers=headers, timeout=60.0
            )
            return 200 <= response.status_code < 300
        except Exception as e:
            logger.error(f"S3 上传失败: {e}")
            return False

    def verify(
        self,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        birth_date: str = None,
        school_id: str = None,
        hcaptcha_token: str = None,
        turnstile_token: str = None,
    ) -> Dict:
        """执行教师验证流程"""
        try:
            current_step = "initial"

            if config.HCAPTCHA_SECRET:
                logger.info("验证 hCaptcha...")
                if not self.verify_hcaptcha(hcaptcha_token):
                    raise Exception("hCaptcha 验证失败")
                logger.info("✅ hCaptcha 验证成功")

            if config.TURNSTILE_SECRET:
                logger.info("验证 Turnstile...")
                if not self.verify_turnstile(turnstile_token):
                    raise Exception("Turnstile 验证失败")
                logger.info("✅ Turnstile 验证成功")

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
                logger.info("申请新的 verificationId ...")
                self.create_verification()

            logger.info(f"教师信息: {first_name} {last_name}")
            logger.info(f"邮箱: {email}")
            logger.info(f"学校: {school['name']}")
            logger.info(f"生日: {birth_date}")
            logger.info(f"验证 ID: {self.verification_id}")

            # 生成教师 PNG
            logger.info("步骤 1/5: 生成教师 PNG 文档...")
            assets = generate_images(first_name, last_name, school_id)
            for asset in assets:
                logger.info(
                    f"  - {asset['file_name']} 大小: {len(asset['data'])/1024:.2f}KB"
                )

            # 提交教师信息
            logger.info("步骤 2/5: 提交教师信息...")
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
                raise Exception(f"步骤 2 失败 (状态码 {step2_status}): {step2_data}")
            if isinstance(step2_data, dict) and step2_data.get("currentStep") == "error":
                error_msg = ", ".join(step2_data.get("errorIds", ["Unknown error"]))
                raise Exception(f"步骤 2 错误: {error_msg}")

            logger.info(f"✅ 步骤 2 完成: {getattr(step2_data, 'get', lambda k, d=None: d)('currentStep')}")
            current_step = (
                step2_data.get("currentStep", current_step) if isinstance(step2_data, dict) else current_step
            )

            # 跳过 SSO（如需要）
            if current_step in ["sso", "collectTeacherPersonalInfo"]:
                logger.info("步骤 3/5: 跳过 SSO 验证...")
                step3_data, _ = self._sheerid_request(
                    "DELETE",
                    f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/sso",
                )
                logger.info(f"✅ 步骤 3 完成: {getattr(step3_data, 'get', lambda k, d=None: d)('currentStep')}")
                current_step = (
                    step3_data.get("currentStep", current_step) if isinstance(step3_data, dict) else current_step
                )

            # 请求上传并上传文档
            logger.info("步骤 4/5: 请求上传 URL ...")
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
                raise Exception(f"未能获取上传 URL: {step4_data}")

            documents = step4_data["documents"]
            if len(documents) != len(assets):
                raise Exception("返回的上传任务数量与文件数量不匹配")

            for doc, asset in zip(documents, assets):
                upload_url = doc.get("uploadUrl")
                if not upload_url:
                    raise Exception("缺少上传 URL")
                if not self._upload_to_s3(upload_url, asset["data"]):
                    raise Exception(f"S3 上传失败: {asset['file_name']}")
                logger.info(f"✅ 已上传 {asset['file_name']}")

            step6_data, _ = self._sheerid_request(
                "POST",
                f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload",
            )
            logger.info(f"✅ 文档提交完成: {getattr(step6_data, 'get', lambda k, d=None: d)('currentStep')}")

            # 获取最终状态（包含 rewardCode）
            final_status, _ = self._sheerid_request(
                "GET",
                f"{config.MY_SHEERID_URL}/rest/v2/verification/{self.verification_id}",
            )
            reward_code = None
            if isinstance(final_status, dict):
                reward_code = final_status.get("rewardCode") or final_status.get("rewardData", {}).get("rewardCode")

            return {
                "success": True,
                "pending": final_status.get("currentStep") != "success" if isinstance(final_status, dict) else True,
                "message": "文档已提交，等待审核"
                if not isinstance(final_status, dict) or final_status.get("currentStep") != "success"
                else "验证成功",
                "verification_id": self.verification_id,
                "redirect_url": final_status.get("redirectUrl") if isinstance(final_status, dict) else None,
                "reward_code": reward_code,
                "status": final_status,
            }

        except Exception as e:
            logger.error(f"❌ 验证失败: {e}")
            return {"success": False, "message": str(e), "verification_id": self.verification_id}


def main():
    """主函数 - 命令行界面"""
    import sys

    print("=" * 60)
    print("SheerID 教师身份验证工具 (Python版)")
    print("=" * 60)
    print()

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("请输入 SheerID 验证入口链接 (含 externalUserId): ").strip()

    if not url:
        print("❌ 错误: 未提供 URL")
        sys.exit(1)

    verification_id = SheerIDVerifier.parse_verification_id(url)
    verifier = SheerIDVerifier(url, verification_id=verification_id)

    print(f"👉 使用链接: {verifier.install_page_url}")
    if verifier.verification_id:
        print(f"已解析 verificationId: {verifier.verification_id}")
    if verifier.external_user_id:
        print(f"externalUserId: {verifier.external_user_id}")
    print()

    result = verifier.verify()

    print()
    print("=" * 60)
    print("验证结果:")
    print("=" * 60)
    print(f"状态: {'✅ 成功' if result['success'] else '❌ 失败'}")
    print(f"消息: {result['message']}")
    if result.get("reward_code"):
        print(f"优惠码: {result['reward_code']}")
    if result.get("redirect_url"):
        print(f"跳转 URL: {result['redirect_url']}")
    print("=" * 60)

    return 0 if result["success"] else 1


if __name__ == "__main__":
    exit(main())
