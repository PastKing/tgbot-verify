"""Bộ tạo tên ngẫu nhiên"""
import random


class NameGenerator:
    """Bộ tạo tên tiếng Anh"""
    
    ROOTS = {
        'prefixes': ['Al', 'Bri', 'Car', 'Dan', 'El', 'Fer', 'Gar', 'Har', 'Jes', 'Kar', 
                    'Lar', 'Mar', 'Nor', 'Par', 'Quin', 'Ros', 'Sar', 'Tar', 'Val', 'Wil'],
        'middles': ['an', 'en', 'in', 'on', 'ar', 'er', 'or', 'ur', 'al', 'el', 
                   'il', 'ol', 'am', 'em', 'im', 'om', 'ay', 'ey', 'oy', 'ian'],
        'suffixes': ['ton', 'son', 'man', 'ley', 'field', 'ford', 'wood', 'stone', 'worth', 'berg',
                    'stein', 'bach', 'heim', 'gard', 'land', 'wick', 'shire', 'dale', 'brook', 'ridge'],
        'name_roots': ['Alex', 'Bern', 'Crist', 'Dav', 'Edw', 'Fred', 'Greg', 'Henr', 'Ivan', 'John',
                      'Ken', 'Leon', 'Mich', 'Nick', 'Oliv', 'Paul', 'Rich', 'Step', 'Thom', 'Will'],
        'name_endings': ['a', 'e', 'i', 'o', 'y', 'ie', 'ey', 'an', 'en', 'in', 
                        'on', 'er', 'ar', 'or', 'el', 'al', 'iel', 'ael', 'ine', 'lyn']
    }
    
    PATTERNS = {
        'first_name': [
            ['prefix', 'ending'],
            ['name_root', 'ending'],
            ['prefix', 'middle', 'ending'],
            ['name_root', 'middle', 'ending']
        ],
        'last_name': [
            ['prefix', 'suffix'],
            ['name_root', 'suffix'],
            ['prefix', 'middle', 'suffix'],
            ['compound']
        ]
    }
    
    @classmethod
    def _generate_component(cls, pattern):
        """Tạo thành phần tên theo mẫu"""
        components = []
        for part in pattern:
            if part == 'prefix':
                component = random.choice(cls.ROOTS['prefixes'])
            elif part == 'middle':
                component = random.choice(cls.ROOTS['middles'])
            elif part == 'suffix':
                component = random.choice(cls.ROOTS['suffixes'])
            elif part == 'name_root':
                component = random.choice(cls.ROOTS['name_roots'])
            elif part == 'ending':
                component = random.choice(cls.ROOTS['name_endings'])
            elif part == 'compound':
                part1 = random.choice(cls.ROOTS['prefixes'])
                part2 = random.choice(cls.ROOTS['suffixes'])
                component = part1 + part2
            else:
                component = ''
            
            components.append(component)
        
        return ''.join(components)
    
    @classmethod
    def _format_name(cls, name):
        """Định dạng tên (viết hoa chữ cái đầu)"""
        return name.capitalize()
    
    @classmethod
    def generate(cls):
        """
        Tạo ngẫu nhiên tên tiếng Anh
        
        Returns:
            dict: Chứa first_name, last_name, full_name
        """
        first_name_pattern = random.choice(cls.PATTERNS['first_name'])
        last_name_pattern = random.choice(cls.PATTERNS['last_name'])
        
        first_name = cls._generate_component(first_name_pattern)
        last_name = cls._generate_component(last_name_pattern)
        
        return {
            'first_name': cls._format_name(first_name),
            'last_name': cls._format_name(last_name),
            'full_name': f"{cls._format_name(first_name)} {cls._format_name(last_name)}"
        }


def generate_email():
    """
    Tạo email ngẫu nhiên (dạng email thường dùng cho giáo viên)

    Returns:
        str: Địa chỉ email
    """
    name = NameGenerator.generate()
    first_name = name['first_name'].lower()
    last_name = name['last_name'].lower()
    random_num = random.randint(1000, 9999)
    domains = ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com', 'icloud.com']
    domain = random.choice(domains)
    return f"{first_name}.{last_name}{random_num}@{domain}"


def generate_birth_date():
    """
    Tạo ngày sinh ngẫu nhiên (độ tuổi giáo viên 1970-1990)

    Returns:
        str: Ngày theo định dạng YYYY-MM-DD
    """
    year = random.randint(1970, 1990)
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    return f"{year}-{month}-{day}"

