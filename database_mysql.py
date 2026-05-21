"""Triển khai cơ sở dữ liệu MySQL

Sử dụng máy chủ MySQL được cung cấp để lưu trữ dữ liệu
"""
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

# Nạp biến môi trường
load_dotenv()

logger = logging.getLogger(__name__)


class MySQLDatabase:
    """Lớp quản lý cơ sở dữ liệu MySQL"""

    def __init__(self):
        """Khởi tạo kết nối cơ sở dữ liệu"""
        import os
        
        # Đọc cấu hình từ biến môi trường (khuyến nghị) hoặc dùng giá trị mặc định
        self.config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'user': os.getenv('MYSQL_USER', 'tgbot_user'),
            'password': os.getenv('MYSQL_PASSWORD', 'your_password_here'),
            'database': os.getenv('MYSQL_DATABASE', 'tgbot_verify'),
            'charset': 'utf8mb4',
            'autocommit': False,
        }
        logger.info(f"Khởi tạo MySQL: {self.config['user']}@{self.config['host']}/{self.config['database']}")
        self.init_database()

    def get_connection(self):
        """Lấy kết nối cơ sở dữ liệu"""
        return pymysql.connect(**self.config)

    def init_database(self):
        """Khởi tạo cấu trúc bảng cơ sở dữ liệu"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Bảng người dùng
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username VARCHAR(255),
                    full_name VARCHAR(255),
                    balance INT DEFAULT 1,
                    is_blocked TINYINT(1) DEFAULT 0,
                    invited_by BIGINT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_checkin DATETIME NULL,
                    INDEX idx_username (username),
                    INDEX idx_invited_by (invited_by)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )

            # Bảng ghi nhận lời mời
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS invitations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    inviter_id BIGINT NOT NULL,
                    invitee_id BIGINT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_inviter (inviter_id),
                    INDEX idx_invitee (invitee_id),
                    FOREIGN KEY (inviter_id) REFERENCES users(user_id),
                    FOREIGN KEY (invitee_id) REFERENCES users(user_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )

            # Bảng ghi nhận xác thực
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS verifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    verification_type VARCHAR(50) NOT NULL,
                    verification_url TEXT,
                    verification_id VARCHAR(255),
                    status VARCHAR(50) NOT NULL,
                    result TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_user_id (user_id),
                    INDEX idx_type (verification_type),
                    INDEX idx_created (created_at),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )

            # Bảng mã nạp
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS card_keys (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    key_code VARCHAR(100) UNIQUE NOT NULL,
                    balance INT NOT NULL,
                    max_uses INT DEFAULT 1,
                    current_uses INT DEFAULT 0,
                    expire_at DATETIME NULL,
                    created_by BIGINT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_key_code (key_code),
                    INDEX idx_created_by (created_by)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )

            # Bảng lịch sử sử dụng mã nạp
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS card_key_usage (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    key_code VARCHAR(100) NOT NULL,
                    user_id BIGINT NOT NULL,
                    used_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_key_code (key_code),
                    INDEX idx_user_id (user_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )

            conn.commit()
            logger.info("Khởi tạo bảng MySQL hoàn tất")

        except Exception as e:
            logger.error(f"Khởi tạo cơ sở dữ liệu thất bại: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def create_user(
        self, user_id: int, username: str, full_name: str, invited_by: Optional[int] = None
    ) -> bool:
        """Tạo người dùng mới"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO users (user_id, username, full_name, invited_by, created_at)
                VALUES (%s, %s, %s, %s, NOW())
                """,
                (user_id, username, full_name, invited_by),
            )

            if invited_by:
                cursor.execute(
                    "UPDATE users SET balance = balance + 2 WHERE user_id = %s",
                    (invited_by,),
                )

                cursor.execute(
                    """
                    INSERT INTO invitations (inviter_id, invitee_id, created_at)
                    VALUES (%s, %s, NOW())
                    """,
                    (invited_by, user_id),
                )

            conn.commit()
            return True

        except pymysql.err.IntegrityError:
            conn.rollback()
            return False
        except Exception as e:
            logger.error(f"Tạo người dùng thất bại: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_user(self, user_id: int) -> Optional[Dict]:
        """Lấy thông tin người dùng"""
        conn = self.get_connection()
        cursor = conn.cursor(DictCursor)

        try:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            row = cursor.fetchone()
            
            if row:
                # Tạo dict mới và chuyển datetime sang chuỗi ISO
                result = dict(row)
                if result.get('created_at'):
                    result['created_at'] = result['created_at'].isoformat()
                if result.get('last_checkin'):
                    result['last_checkin'] = result['last_checkin'].isoformat()
                return result
            return None

        finally:
            cursor.close()
            conn.close()

    def user_exists(self, user_id: int) -> bool:
        """Kiểm tra người dùng có tồn tại hay không"""
        return self.get_user(user_id) is not None

    def is_user_blocked(self, user_id: int) -> bool:
        """Kiểm tra người dùng có bị chặn hay không"""
        user = self.get_user(user_id)
        return user and user["is_blocked"] == 1

    def block_user(self, user_id: int) -> bool:
        """Chặn người dùng"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE users SET is_blocked = 1 WHERE user_id = %s", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Chặn người dùng thất bại: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def unblock_user(self, user_id: int) -> bool:
        """Bỏ chặn người dùng"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE users SET is_blocked = 0 WHERE user_id = %s", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Bỏ chặn thất bại: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_blacklist(self) -> List[Dict]:
        """Lấy danh sách chặn"""
        conn = self.get_connection()
        cursor = conn.cursor(DictCursor)

        try:
            cursor.execute("SELECT * FROM users WHERE is_blocked = 1")
            return list(cursor.fetchall())
        finally:
            cursor.close()
            conn.close()

    def add_balance(self, user_id: int, amount: int) -> bool:
        """Tăng điểm cho người dùng"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE users SET balance = balance + %s WHERE user_id = %s",
                (amount, user_id),
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Tăng điểm thất bại: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def deduct_balance(self, user_id: int, amount: int) -> bool:
        """Trừ điểm của người dùng"""
        user = self.get_user(user_id)
        if not user or user["balance"] < amount:
            return False

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE users SET balance = balance - %s WHERE user_id = %s",
                (amount, user_id),
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Trừ điểm thất bại: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def can_checkin(self, user_id: int) -> bool:
        """Kiểm tra hôm nay người dùng có thể điểm danh hay không"""
        user = self.get_user(user_id)
        if not user:
            return False

        last_checkin = user.get("last_checkin")
        if not last_checkin:
            return True

        last_date = datetime.fromisoformat(last_checkin).date()
        today = datetime.now().date()

        return last_date < today

    def checkin(self, user_id: int) -> bool:
        """Người dùng điểm danh (sửa lỗi điểm danh vô hạn)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Dùng thao tác SQL nguyên tử để tránh điều kiện tranh chấp
            # Chỉ cập nhật khi last_checkin là NULL hoặc ngày < hôm nay
            cursor.execute(
                """
                UPDATE users
                SET balance = balance + 1, last_checkin = NOW()
                WHERE user_id = %s 
                AND (
                    last_checkin IS NULL 
                    OR DATE(last_checkin) < CURDATE()
                )
                """,
                (user_id,),
            )
            conn.commit()
            
            # Kiểm tra xem có thực sự cập nhật hay không (affected_rows > 0 nghĩa là điểm danh thành công)
            success = cursor.rowcount > 0
            return success
            
        except Exception as e:
            logger.error(f"Điểm danh thất bại: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def add_verification(
        self, user_id: int, verification_type: str, verification_url: str,
        status: str, result: str = "", verification_id: str = ""
    ) -> bool:
        """Thêm bản ghi xác thực"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO verifications
                (user_id, verification_type, verification_url, verification_id, status, result, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """,
                (user_id, verification_type, verification_url, verification_id, status, result),
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Thêm bản ghi xác thực thất bại: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_user_verifications(self, user_id: int) -> List[Dict]:
        """Lấy bản ghi xác thực của người dùng"""
        conn = self.get_connection()
        cursor = conn.cursor(DictCursor)

        try:
            cursor.execute(
                """
                SELECT * FROM verifications
                WHERE user_id = %s
                ORDER BY created_at DESC
                """,
                (user_id,),
            )
            return list(cursor.fetchall())
        finally:
            cursor.close()
            conn.close()

    def create_card_key(
        self, key_code: str, balance: int, created_by: int,
        max_uses: int = 1, expire_days: Optional[int] = None
    ) -> bool:
        """Tạo mã nạp"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            expire_at = None
            if expire_days:
                expire_at = datetime.now() + timedelta(days=expire_days)

            cursor.execute(
                """
                INSERT INTO card_keys (key_code, balance, max_uses, created_by, created_at, expire_at)
                VALUES (%s, %s, %s, %s, NOW(), %s)
                """,
                (key_code, balance, max_uses, created_by, expire_at),
            )
            conn.commit()
            return True

        except pymysql.err.IntegrityError:
            logger.error(f"Mã nạp đã tồn tại: {key_code}")
            conn.rollback()
            return False
        except Exception as e:
            logger.error(f"Tạo mã nạp thất bại: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def use_card_key(self, key_code: str, user_id: int) -> Optional[int]:
        """Dùng mã nạp, trả về số điểm nhận được"""
        conn = self.get_connection()
        cursor = conn.cursor(DictCursor)

        try:
            # Tra cứu mã nạp
            cursor.execute(
                "SELECT * FROM card_keys WHERE key_code = %s",
                (key_code,),
            )
            card = cursor.fetchone()

            if not card:
                return None

            # Kiểm tra đã hết hạn hay chưa
            if card["expire_at"] and datetime.now() > card["expire_at"]:
                return -2

            # Kiểm tra số lần sử dụng
            if card["current_uses"] >= card["max_uses"]:
                return -1

            # Kiểm tra người dùng đã dùng mã nạp này hay chưa
            cursor.execute(
                "SELECT COUNT(*) as count FROM card_key_usage WHERE key_code = %s AND user_id = %s",
                (key_code, user_id),
            )
            count = cursor.fetchone()
            if count['count'] > 0:
                return -3

            # Cập nhật số lần sử dụng
            cursor.execute(
                "UPDATE card_keys SET current_uses = current_uses + 1 WHERE key_code = %s",
                (key_code,),
            )

            # Ghi lại lịch sử sử dụng
            cursor.execute(
                "INSERT INTO card_key_usage (key_code, user_id, used_at) VALUES (%s, %s, NOW())",
                (key_code, user_id),
            )

            # Cộng điểm cho người dùng
            cursor.execute(
                "UPDATE users SET balance = balance + %s WHERE user_id = %s",
                (card["balance"], user_id),
            )

            conn.commit()
            return card["balance"]

        except Exception as e:
            logger.error(f"Dùng mã nạp thất bại: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def get_card_key_info(self, key_code: str) -> Optional[Dict]:
        """Lấy thông tin mã nạp"""
        conn = self.get_connection()
        cursor = conn.cursor(DictCursor)

        try:
            cursor.execute("SELECT * FROM card_keys WHERE key_code = %s", (key_code,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_all_card_keys(self, created_by: Optional[int] = None) -> List[Dict]:
        """Lấy tất cả mã nạp (có thể lọc theo người tạo)"""
        conn = self.get_connection()
        cursor = conn.cursor(DictCursor)

        try:
            if created_by:
                cursor.execute(
                    "SELECT * FROM card_keys WHERE created_by = %s ORDER BY created_at DESC",
                    (created_by,),
                )
            else:
                cursor.execute("SELECT * FROM card_keys ORDER BY created_at DESC")
            
            return list(cursor.fetchall())
        finally:
            cursor.close()
            conn.close()

    def get_all_user_ids(self) -> List[int]:
        """Lấy tất cả user_id"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT user_id FROM users")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        finally:
            cursor.close()
            conn.close()


# Tạo bí danh cho thể hiện toàn cục để giữ tương thích với phiên bản SQLite
Database = MySQLDatabase

