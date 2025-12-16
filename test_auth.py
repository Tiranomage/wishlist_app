#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы аутентификации
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_registration_and_login():
    # Тестовые данные
    test_email = "test@example.com"
    test_password = "password123"
    
    print("Тестирование регистрации...")
    
    # Регистрация
    register_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Регистрация - Статус: {register_response.status_code}")
        print(f"Регистрация - Ответ: {register_response.text}")
        
        if register_response.status_code == 201:
            print("✓ Регистрация прошла успешно")
        else:
            print("✗ Ошибка регистрации")
            
    except Exception as e:
        print(f"Ошибка при регистрации: {e}")
        return
    
    print("\nТестирование входа...")
    
    # Вход
    login_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Вход - Статус: {login_response.status_code}")
        print(f"Вход - Ответ: {login_response.text}")
        
        if login_response.status_code == 200:
            tokens = login_response.json()
            access_token = tokens.get("access_token")
            print("✓ Вход прошел успешно")
            
            # Тестирование защищенного маршрута
            print("\nТестирование доступа к защищенному маршруту...")
            headers = {"Authorization": f"Bearer {access_token}"}
            me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            print(f"GET /auth/me - Статус: {me_response.status_code}")
            print(f"GET /auth/me - Ответ: {me_response.text}")
            
            if me_response.status_code == 200:
                print("✓ Доступ к защищенному маршруту получен успешно")
            else:
                print("✗ Ошибка доступа к защищенному маршруту")
        else:
            print("✗ Ошибка входа")
            
    except Exception as e:
        print(f"Ошибка при входе: {e}")

if __name__ == "__main__":
    test_registration_and_login()