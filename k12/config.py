# SheerID 教师验证配置文件

# SheerID API 配置
PROGRAM_ID = '68d47554aa292d20b9bec8f7'
SHEERID_BASE_URL = 'https://services.sheerid.com'
MY_SHEERID_URL = 'https://my.sheerid.com'

# 验证码配置（留空关闭）
HCAPTCHA_SECRET = ''  # 留空关闭 hCaptcha 验证
TURNSTILE_SECRET = ''  # 留空关闭 Turnstile 验证

# 文件大小限制
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

# 学校配置（高中）
SCHOOLS = {
    '3995910': {
        'id': 3995910,
        'idExtended': '3995910',
        'name': 'Springfield High School (Springfield, OR)',
        'country': 'US',
        'type': 'HIGH_SCHOOL'
    },
    '3995271': {
        'id': 3995271,
        'idExtended': '3995271',
        'name': 'Springfield High School (Springfield, OH)',
        'country': 'US',
        'type': 'HIGH_SCHOOL'
    },
    '3992142': {
        'id': 3992142,
        'idExtended': '3992142',
        'name': 'Springfield High School (Springfield, IL)',
        'country': 'US',
        'type': 'HIGH_SCHOOL'
    },
    '3996208': {
        'id': 3996208,
        'idExtended': '3996208',
        'name': 'Springfield High School (Springfield, PA)',
        'country': 'US',
        'type': 'HIGH_SCHOOL'
    },
    '4015002': {
        'id': 4015002,
        'idExtended': '4015002',
        'name': 'Springfield High School (Springfield, TN)',
        'country': 'US',
        'type': 'HIGH_SCHOOL'
    },
    '4015001': {
        'id': 4015001,
        'idExtended': '4015001',
        'name': 'Springfield High School (Springfield, VT)',
        'country': 'US',
        'type': 'HIGH_SCHOOL'
    },
    '4014999': {
        'id': 4014999,
        'idExtended': '4014999',
        'name': 'Springfield High School (Springfield, LA)',
        'country': 'US',
        'type': 'HIGH_SCHOOL'
    },
    
}

# 默认学校
DEFAULT_SCHOOL_ID = '3995910'


