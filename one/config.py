# File cấu hình xác thực SheerID

# Cấu hình SheerID API
PROGRAM_ID = '67c8c14f5f17a83b745e3f82'
SHEERID_BASE_URL = 'https://services.sheerid.com'
MY_SHEERID_URL = 'https://my.sheerid.com'

# Giới hạn kích thước tệp
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

# Cấu hình trường - nhiều cơ sở của Pennsylvania State University
SCHOOLS = {
    '2565': {
        'id': 2565,
        'idExtended': '2565',
        'name': 'Pennsylvania State University-Main Campus',
        'city': 'University Park',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'PSU.EDU',
        'latitude': 40.798214,
        'longitude': -77.85991
    },
    '651379': {
        'id': 651379,
        'idExtended': '651379',
        'name': 'Pennsylvania State University-World Campus',
        'city': 'University Park',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'PSU.EDU',
        'latitude': 40.832783,
        'longitude': -77.84159
    },
    '8387': {
        'id': 8387,
        'idExtended': '8387',
        'name': 'Pennsylvania State University-Penn State Harrisburg',
        'city': 'Middletown',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'PSU.EDU',
        'latitude': 40.204082,
        'longitude': -76.74168
    },
    '8382': {
        'id': 8382,
        'idExtended': '8382',
        'name': 'Pennsylvania State University-Penn State Altoona',
        'city': 'Altoona',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'PSU.EDU',
        'latitude': 40.54092,
        'longitude': -78.40825
    },
    '8396': {
        'id': 8396,
        'idExtended': '8396',
        'name': 'Pennsylvania State University-Penn State Berks',
        'city': 'Reading',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'PSU.EDU',
        'latitude': 40.359947,
        'longitude': -75.97615
    },
    '8379': {
        'id': 8379,
        'idExtended': '8379',
        'name': 'Pennsylvania State University-Penn State Brandywine',
        'city': 'Media',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'PSU.EDU',
        'latitude': 39.92638,
        'longitude': -75.44698
    },
    '2560': {
        'id': 2560,
        'idExtended': '2560',
        'name': 'Pennsylvania State University-College of Medicine',
        'city': 'Hershey',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'PSU.EDU',
        'latitude': 40.264244,
        'longitude': -76.67408
    },
    '650600': {
        'id': 650600,
        'idExtended': '650600',
        'name': 'Pennsylvania State University-Penn State Lehigh Valley',
        'city': 'Center Valley',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'PSU.EDU',
        'latitude': 40.559208,
        'longitude': -75.402504
    },
    '8388': {
        'id': 8388,
        'idExtended': '8388',
        'name': 'Pennsylvania State University-Penn State Hazleton',
        'city': 'Hazleton',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'PSU.EDU',
        'latitude': 40.98396,
        'longitude': -76.03106
    },
    '8394': {
        'id': 8394,
        'idExtended': '8394',
        'name': 'Pennsylvania State University-Penn State Worthington Scranton',
        'city': 'Dunmore',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'PSU.EDU',
        'latitude': 41.440258,
        'longitude': -75.62058
    }
}

# Trường mặc định
DEFAULT_SCHOOL_ID = '2565'

# Tham số UTM (tham số theo dõi marketing)
# Nếu URL không có các tham số này, chúng sẽ được tự động thêm vào
DEFAULT_UTM_PARAMS = {
    'utm_source': 'gemini',
    'utm_medium': 'paid_media',
    'utm_campaign': 'students_pmax_bts-slap'
}

