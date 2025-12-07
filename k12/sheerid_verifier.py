"""SheerID 教师验证主程序"""
import re
import random
import logging
import httpx
from typing import Dict, Optional, Tuple

# 支持既作为包导入又直接脚本运行
try:
    from . import config  # type: ignore
    from .name_generator import NameGenerator, generate_email, generate_birth_date  # type: ignore
    from .img_generator import generate_teacher_pdf, generate_teacher_png  # type: ignore
except ImportError:
    import config  # type: ignore
    from name_generator import NameGenerator, generate_email, generate_birth_date  # type: ignore
    from img_generator import generate_teacher_pdf, generate_teacher_png  # type: ignore

# 导入配置常量
PROGRAM_ID = config.PROGRAM_ID
SHEERID_BASE_URL = config.SHEERID_BASE_URL
MY_SHEERID_URL = config.MY_SHEERID_URL
HCAPTCHA_SECRET = config.HCAPTCHA_SECRET
TURNSTILE_SECRET = config.TURNSTILE_SECRET
SCHOOLS = config.SCHOOLS
DEFAULT_SCHOOL_ID = config.DEFAULT_SCHOOL_ID


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class SheerIDVerifier:
    """SheerID 教师身份验证器"""

    def __init__(self, verification_id: str):
        """
        初始化验证器

        Args:
            verification_id: SheerID 验证 ID
        """
        self.verification_id = verification_id
        self.device_fingerprint = self._generate_device_fingerprint()
        self.http_client = httpx.Client(timeout=30.0)

    def __del__(self):
        """清理 HTTP 客户端"""
        if hasattr(self, 'http_client'):
            self.http_client.close()

    @staticmethod
    def _generate_device_fingerprint() -> str:
        """生成设备指纹"""
        chars = '0123456789abcdef'
        return ''.join(random.choice(chars) for _ in range(32))

    @staticmethod
    def normalize_url(url: str) -> str:
        """规范化 URL"""
        return url

    @staticmethod
    def parse_verification_id(url: str) -> Optional[str]:
        """从 URL 中解析验证 ID"""
        match = re.search(r'verificationId=([a-f0-9]+)', url, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def verify_hcaptcha(self, token: str) -> bool:
        """验证 hCaptcha token"""
        if not HCAPTCHA_SECRET or not token:
            return not HCAPTCHA_SECRET

        try:
            response = self.http_client.post(
                'https://hcaptcha.com/siteverify',
                data={
                    'response': token,
                    'secret': HCAPTCHA_SECRET
                },
                headers=headers
            )
            result = response.json()
            return result.get('success', False)
        except Exception as e:
            logger.error(f"hCaptcha 验证失败: {e}")
            return False

    def verify_turnstile(self, token: str) -> bool:
        """验证 Turnstile token"""
        if not TURNSTILE_SECRET or not token:
            return not TURNSTILE_SECRET

        try:
            response = self.http_client.post(
                'https://challenges.cloudflare.com/turnstile/v0/siteverify',
                data={
                    'secret': TURNSTILE_SECRET,
                    'response': token
                }
            )
            result = response.json()
            return result.get('success', False)
        except Exception as e:
            logger.error(f"Turnstile 验证失败: {e}")
            return False

    def _sheerid_request(self, method: str, url: str,
                         body: Optional[Dict] = None) -> Tuple[Dict, int]:
        """
        发送 SheerID API 请求
        """
        headers = {
            'Content-Type': 'application/json',
        }

        try:
            response = self.http_client.request(
                method=method,
                url=url,
                json=body,
                headers=headers
            )

            try:
                data = response.json()
            except Exception:
                data = response.text

            return data, response.status_code
        except Exception as e:
            logger.error(f"SheerID 请求失败: {e}")
            raise

    def _upload_to_s3(self, upload_url: str, content: bytes, mime_type: str) -> bool:
        """
        上传文件到 S3
        """
        try:
            headers = {
                'Content-Type': mime_type,
            }
            response = self.http_client.put(
                upload_url,
                content=content,
                headers=headers,
                timeout=60.0
            )
            return 200 <= response.status_code < 300
        except Exception as e:
            logger.error(f"S3 上传失败: {e}")
            return False

    def verify(self, first_name: str = None, last_name: str = None,
               email: str = None, birth_date: str = None,
               school_id: str = None,
               hcaptcha_token: str = None, turnstile_token: str = None) -> Dict:
        """
        执行完整的验证流程，移除状态轮询以减少耗时
        """
        try:
            current_step = 'initial'

            # 验证码检查（如果启用）
            if HCAPTCHA_SECRET:
                logger.info("验证 hCaptcha...")
                if not self.verify_hcaptcha(hcaptcha_token):
                    raise Exception("hCaptcha 验证失败")
                logger.info("✓ hCaptcha 验证成功")

            if TURNSTILE_SECRET:
                logger.info("验证 Turnstile...")
                if not self.verify_turnstile(turnstile_token):
                    raise Exception("Turnstile 验证失败")
                logger.info("✓ Turnstile 验证成功")

            # 生成教师信息
            if not first_name or not last_name:
                name = NameGenerator.generate()
                first_name = name['first_name']
                last_name = name['last_name']

            school_id = school_id or DEFAULT_SCHOOL_ID
            school = SCHOOLS[school_id]

            if not email:
                email = generate_email()

            if not birth_date:
                birth_date = generate_birth_date()

            logger.info(f"教师信息: {first_name} {last_name}")
            logger.info(f"邮箱: {email}")
            logger.info(f"学校: {school['name']}")
            logger.info(f"生日: {birth_date}")
            logger.info(f"验证 ID: {self.verification_id}")

            # 生成教师证明 PDF + PNG
            logger.info("步骤 1/4: 生成教师证明 PDF 和 PNG...")
            pdf_data = generate_teacher_pdf(first_name, last_name)
            png_data = generate_teacher_png(first_name, last_name)
            pdf_size = len(pdf_data)
            png_size = len(png_data)
            logger.info(f"✓ PDF 大小: {pdf_size / 1024:.2f}KB, PNG 大小: {png_size / 1024:.2f}KB")

            # 步骤 2: 提交教师信息
            logger.info("步骤 2/4: 提交教师信息...")
            step2_body = {
                'firstName': first_name,
                'lastName': last_name,
                'birthDate': birth_date,
                'email': email,
                'phoneNumber': '',
                'organization': {
                    'id': school['id'],
                    'idExtended': school['idExtended'],
                    'name': school['name']
                },
                'deviceFingerprintHash': self.device_fingerprint,
                'locale': 'en-US',
                'metadata': {
                    'marketConsentValue': False,
                    'refererUrl': f"{SHEERID_BASE_URL}/verify/{PROGRAM_ID}/?verificationId={self.verification_id}",
                    'verificationId': self.verification_id,
                    'submissionOptIn': 'By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount'
                }
            }

            step2_data, step2_status = self._sheerid_request(
                'POST',
                f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectTeacherPersonalInfo",
                step2_body
            )

            if step2_status != 200:
                raise Exception(f"步骤 2 失败 (状态码 {step2_status}): {step2_data}")

            if step2_data.get('currentStep') == 'error':
                error_msg = ', '.join(step2_data.get('errorIds', ['Unknown error']))
                raise Exception(f"步骤 2 错误: {error_msg}")

            logger.info(f"✓ 步骤 2 完成: {step2_data.get('currentStep')}")
            current_step = step2_data.get('currentStep', current_step)

            # 步骤 3: 跳过 SSO（如果需要）
            if current_step in ['sso', 'collectTeacherPersonalInfo']:
                logger.info("步骤 3/4: 跳过 SSO 验证...")
                step3_data, _ = self._sheerid_request(
                    'DELETE',
                    f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/sso"
                )
                logger.info(f"✓ 步骤 3 完成: {step3_data.get('currentStep')}")
                current_step = step3_data.get('currentStep', current_step)

            # 步骤 4: 上传文档并完成提交
            logger.info("步骤 4/4: 请求并上传文档...")
            step4_body = {
                'files': [
                    {
                        'fileName': 'teacher_document.pdf',
                        'mimeType': 'application/pdf',
                        'fileSize': pdf_size
                    },
                    {
                        'fileName': 'teacher_document.png',
                        'mimeType': 'image/png',
                        'fileSize': png_size
                    }
                ]
            }

            step4_data, step4_status = self._sheerid_request(
                'POST',
                f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload",
                step4_body
            )

            documents = step4_data.get('documents') or []
            if len(documents) < 2:
                raise Exception("未能获取上传 URL")

            pdf_upload_url = documents[0]['uploadUrl']
            png_upload_url = documents[1]['uploadUrl']
            logger.info("✓ 获取上传 URL 成功")

            if not self._upload_to_s3(pdf_upload_url, pdf_data, 'application/pdf'):
                raise Exception("PDF 上传失败")
            if not self._upload_to_s3(png_upload_url, png_data, 'image/png'):
                raise Exception("PNG 上传失败")
            logger.info("✓ 教师证明 PDF/PNG 上传成功")

            step6_data, _ = self._sheerid_request(
                'POST',
                f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload"
            )
            logger.info(f"✓ 文档提交完成: {step6_data.get('currentStep')}")
            final_status = step6_data

            # 不做状态轮询，直接返回等待审核
            return {
                'success': True,
                'pending': True,
                'message': '文档已提交，等待审核',
                'verification_id': self.verification_id,
                'redirect_url': final_status.get('redirectUrl'),
                'status': final_status
            }

        except Exception as e:
            logger.error(f"✗ 验证失败: {e}")
            return {
                'success': False,
                'message': str(e),
                'verification_id': self.verification_id
            }
