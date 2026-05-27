import pytest
from src.api.v1.endpoints.user1c import transform_1c_data

def test_transform_1c_data_success():
    # Имитируем "грязные" данные из 1С
    raw_data = [
        {'Телефон': '89001112233', 'НомерДоговора': '123', 'Баланс': ''},
        {'Телефон': '+79990001122', 'НомерДоговора': '456', 'Баланс': '-500.00'}
    ]
    
    result = transform_1c_data(raw_data)
    
    # ПРОВЕРКИ (Asserts):
    assert len(result) == 2
    # Проверяем замену 8 на 7
    assert result[0]['phone'] == '79001112233'
    # Проверяем замену пустой строки на ноль
    assert result[0]['dolg'] == '0.00'
    # Проверяем +7 -> 7
    assert result[1]['phone'] == '79990001122'

def test_transform_1c_data_with_trash():
    # Проверяем, что функция не упадет, если придет строка вместо словаря
    raw_data = ["какой-то мусор", {"Телефон": "8123", "Баланс": "100"}]
    
    result = transform_1c_data(raw_data)
    
    # Должен остаться только 1 валидный объект, строка должна проигнорироваться
    assert len(result) == 1
    assert result[0]['phone'] == '7123'
