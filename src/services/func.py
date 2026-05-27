import re
from tortoise.expressions import Q
import secrets


def checkPhone(phone):
    try:
        if phone.startswith(('+7', '+8', '8')):
            if phone.startswith('+'):
                phone = "7"+phone[2:]
            else: 
                phone = "7"+phpne[1:] 
        return phone
    except Exception as error:
        print(error)


 


def normalize_phone(phone: str) -> str:
    """Приводит телефон к единому формату (10 цифр без кода страны)"""
    if not phone:
        return ""
    
    # Удаляем всё, кроме цифр
    digits = re.sub(r'\D', '', phone)
    
    # Если 11 цифр и начинается с 7 или 8 - убираем первую
    if len(digits) == 11 and digits[0] in ('7', '8'):
        return digits[1:]  # 10 цифр без кода страны
    # Если 10 цифр - возвращаем как есть
    elif len(digits) == 10:
        return digits
    # Если 12 цифр и начинается с +7
    elif len(digits) == 12 and digits.startswith('7'):
        return digits[2:]  # убираем +7
    
    return digits  

def generate_phone_variants(phone: str) -> list:
    """Генерирует все возможные варианты написания номера"""
    clean_phone = normalize_phone(phone)
    if not clean_phone:
        return []
    
    variants = [
        clean_phone,                    
        f"7{clean_phone}",              
        f"8{clean_phone}",              
        f"+7{clean_phone}",             
        f"+7 ({clean_phone[:3]}) {clean_phone[3:6]}-{clean_phone[6:8]}-{clean_phone[8:]}",  
        f"8 ({clean_phone[:3]}) {clean_phone[3:6]}-{clean_phone[6:8]}-{clean_phone[8:]}",   
    ]
    return variants



    

def generate_numeric_code(length: int = 4) -> str:
    # Генерируем число от 0 до 999,999
    code = secrets.randbelow(10**length)
    # Форматируем в строку, добавляя нули слева (например, "001234")
    return str(code).zfill(length)