#!/usr/bin/env python3
"""
Тестовый скрипт для проверки системы аутентификации и регистрации
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_registration_and_login():
    print("=== Тестирование регистрации и входа ===")
    
    # Подготовим тестовые данные
    test_email = "testuser@example.com"
    test_password = "securepassword123"
    
    # Шаг 1: Регистрация нового пользователя
    print(f"1. Регистрация пользователя с email: {test_email}")
    register_response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "email": test_email,
            "password": test_password
        }
    )
    print(f"   Статус ответа: {register_response.status_code}")
    if register_response.status_code == 201:
        print(f"   Ответ: {register_response.json()}")
    else:
        print(f"   Ошибка: {register_response.text}")
    
    # Шаг 2: Попытка повторной регистрации с тем же email (должна быть ошибка)
    print(f"\n2. Повторная регистрация с тем же email (ожидается ошибка)")
    duplicate_register_response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "email": test_email,
            "password": test_password
        }
    )
    print(f"   Статус ответа: {duplicate_register_response.status_code}")
    if duplicate_register_response.status_code != 400:
        print("   ОШИБКА: Должна была вернуться ошибка 400 при попытке повторной регистрации!")
    else:
        print(f"   Ответ: {duplicate_register_response.json()}")
    
    # Шаг 3: Вход в систему
    print(f"\n3. Вход в систему с email: {test_email}")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": test_email,
            "password": test_password
        }
    )
    print(f"   Статус ответа: {login_response.status_code}")
    if login_response.status_code == 200:
        login_data = login_response.json()
        print(f"   Ответ: {json.dumps(login_data, indent=2)}")
        
        # Получаем токен
        access_token = login_data.get("access_token")
        if access_token:
            print("\n4. Запрос информации о текущем пользователе")
            me_response = requests.get(
                f"{BASE_URL}/auth/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            print(f"   Статус ответа: {me_response.status_code}")
            if me_response.status_code == 200:
                print(f"   Ответ: {me_response.json()}")
            else:
                print(f"   Ошибка: {me_response.text}")
        else:
            print("   ОШИБКА: Не получен access_token при входе!")
    else:
        print(f"   Ошибка: {login_response.text}")
    
    # Шаг 4: Попытка входа с неверными данными
    print(f"\n5. Вход в систему с неверным паролем")
    invalid_login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": test_email,
            "password": "wrongpassword"
        }
    )
    print(f"   Статус ответа: {invalid_login_response.status_code}")
    if invalid_login_response.status_code == 401:
        print(f"   Ответ: {invalid_login_response.json()}")
    else:
        print("   ОШИБКА: Должна была вернуться ошибка 401 при попытке входа с неверным паролем!")
    
    print("\n=== Тестирование завершено ===")

if __name__ == "__main__":
    test_registration_and_login()