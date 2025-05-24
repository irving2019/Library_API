# 📚 Library Management System API

<div align="center">

![Library Management](https://img.shields.io/badge/Library-Management-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.41-orange)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-100%25-brightgreen)

</div>

<div align="center">

[Обзор](#-обзор-проекта) •
[Установка](#-пошаговое-руководство-по-запуску-и-использованию) •
[Использование](#2-первые-шаги-после-запуска) •
[API Docs](#-api-documentation) •
[Безопасность](#-безопасность) •
[Разработка](#-процесс-разработки)

</div>

</div>

REST API система управления библиотекой с использованием FastAPI и SQLAlchemy.

## 📚 Обзор проекта

Система предоставляет полный набор инструментов для управления библиотекой, включая:
- Управление каталогом книг
- Учет читателей
- Система выдачи и возврата книг
- Отслеживание доступности книг
- Защищенный доступ для библиотекарей

## 🛠 Технический стек

### Основные технологии
- **FastAPI**: Современный, быстрый фреймворк для создания API
- **SQLAlchemy**: Мощный ORM для работы с базой данных
- **Pydantic**: Валидация данных и сериализация
- **Alembic**: Управление миграциями базы данных
- **JWT**: Безопасная аутентификация
- **Docker**: Контейнеризация приложения

### Обоснование выбора технологий
- **FastAPI** выбран за его:
  - Высокую производительность
  - Автоматическую генерацию документации OpenAPI
  - Встроенную валидацию данных
  - Асинхронную поддержку
  
- **SQLAlchemy** предоставляет:
  - Гибкое управление БД
  - Поддержку миграций через Alembic
  - Защиту от SQL-инъекций

## 🔒 Безопасность

### Аутентификация
- Используется JWT (JSON Web Tokens):
  - Безопасное хранение состояния сессии
  - Возможность горизонтального масштабирования
  - Поддержка refresh-токенов

### Хеширование паролей
- **bcrypt** используется для:
  - Надежного хеширования паролей
  - Защиты от атак перебором
  - Автоматического добавления "соли"

## 🔒 Детальное описание системы аутентификации

### Выбор технологий аутентификации

1. **JWT (JSON Web Tokens)**
   - **Почему JWT?**
     - Stateless архитектура - не требует хранения сессий на сервере
     - Масштабируемость - работает в распределенных системах
     - Встроенная поддержка expiration time
     - Возможность хранения дополнительных данных в payload
   
   - **Реализация:**
     ```python
     # Создание токена
     access_token = create_access_token(data={"sub": user.email})
     
     # Проверка токена
     current_user = get_current_user(token)
     ```

2. **Библиотеки**
   - **python-jose[cryptography]**
     - Надежная реализация JWT
     - Поддержка различных алгоритмов шифрования
     - Активное сообщество и обновления
   
   - **passlib[bcrypt]**
     - Современный алгоритм хеширования bcrypt
     - Автоматическое управление солью
     - Настраиваемая сложность хеширования

3. **Защита эндпоинтов**
   - **Публичные эндпоинты:**
     - GET /books (для просмотра каталога)
     - POST /register (регистрация)
     - POST /token (получение токена)
   
   - **Защищенные эндпоинты (требуют JWT):**
     - Все операции с читателями
     - Изменение книг (POST, PUT, DELETE)
     - Операции выдачи/возврата

4. **Процесс аутентификации**
   ```mermaid
   sequenceDiagram
      Client->>Server: POST /token (email + password)
      Server->>Database: Проверка credentials
      Database-->>Server: User exists
      Server->>Server: create_access_token()
      Server-->>Client: JWT Token
      Client->>Server: Request + Bearer Token
      Server->>Server: verify_token()
      Server-->>Client: Protected Resource
   ```

5. **Безопасность**
   - Пароли никогда не хранятся в чистом виде
   - bcrypt автоматически генерирует соль для каждого пароля
   - Токены имеют ограниченное время жизни (30 минут)
   - Все защищенные маршруты проверяются через middleware

### Особенности реализации

1. **Хеширование паролей:**
   ```python
   pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
   hashed_password = pwd_context.hash(password)
   ```

2. **Проверка токена:**
   ```python
   @router.get("/protected")
   async def protected_route(
       current_user: User = Depends(get_current_active_user)
   ):
       return {"message": "Access granted"}
   ```

3. **Обработка ошибок:**
   - 401 для невалидного токена
   - 403 для недостаточных прав
   - Детальные сообщения об ошибках

### Преимущества выбранного подхода

1. **Масштабируемость:**
   - Поддержка микросервисной архитектуры
   - Легкое горизонтальное масштабирование
   - Отсутствие состояния на сервере

2. **Безопасность:**
   - Современные алгоритмы шифрования
   - Защита от основных векторов атак
   - Гибкая настройка прав доступа

3. **Производительность:**
   - Быстрая валидация токенов
   - Минимальная нагрузка на БД
   - Эффективное кэширование

## 📋 Бизнес-логика

### Управление книгами
- **Инвентаризация**:
  - Отслеживание количества копий
  - История выдач/возвратов
  - Автоматический учет доступности

### Правила выдачи
- **Ограничения для читателей**:
  - Максимум 3 книги на руках
  - Проверка просрочек
  - Автоматический расчет даты возврата

## 🚀 Пошаговое руководство по запуску и использованию

### 1. Установка и настройка

#### Docker (рекомендуемый способ)
```bash
# Клонирование репозитория
git clone https://github.com/irving2019/Library_API.git
cd Library_API

# Запуск с Docker
docker-compose up --build
```

#### Локальный запуск
```bash
# 1. Клонирование репозитория
git clone https://github.com/irving2019/Library_API.git
cd Library_API

# 2. Создание виртуального окружения
python -m venv venv
.\venv\Scripts\Activate.ps1  # для Windows
# ИЛИ
source venv/bin/activate     # для Linux/Mac

# 3. Установка зависимостей
pip install -r requirements.txt

# 4. Настройка переменных окружения
# Создайте файл .env со следующим содержимым:
DATABASE_URL=sqlite:///library.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 5. Применение миграций
alembic upgrade head

# 6. Запуск сервера
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Первые шаги после запуска

1. **Откройте документацию API**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

2. **Регистрация библиотекаря (администратора)**:
   ```bash
   curl -X POST "http://localhost:8000/register" \
   -H "Content-Type: application/json" \
   -d '{
     "email": "admin@library.com",
     "password": "SecurePass123!"
   }'
   ```
   
   Или через Swagger UI:
   - Перейдите в раздел Authentication
   - Найдите POST /register
   - Заполните email и password
   - Нажмите "Execute"

3. **Получение JWT токена**:
   ```bash
   curl -X POST "http://localhost:8000/token" \
   -H "Content-Type: application/form-data" \
   -d "username=admin@library.com&password=SecurePass123!"
   ```

   Сохраните полученный токен - он понадобится для дальнейшей работы!

### 3. Основные операции

#### 3.1 Управление книгами

1. **Добавление новой книги**:
   ```bash
   curl -X POST "http://localhost:8000/books/" \
   -H "Authorization: Bearer YOUR_TOKEN" \
   -H "Content-Type: application/json" \
   -d '{
     "title": "1984",
     "author": "George Orwell",
     "publication_year": 1949,
     "isbn": "978-0451524935",
     "copies_available": 5
   }'
   ```

2. **Просмотр списка книг**:
   ```bash
   curl "http://localhost:8000/books/"
   ```

#### 3.2 Управление читателями

1. **Добавление читателя**:
   ```bash
   curl -X POST "http://localhost:8000/readers/" \
   -H "Authorization: Bearer YOUR_TOKEN" \
   -H "Content-Type: application/json" \
   -d '{
     "name": "Иван Петров",
     "email": "ivan@example.com"
   }'
   ```

#### 3.3 Выдача и возврат книг

1. **Выдача книги**:
   ```bash
   curl -X POST "http://localhost:8000/borrow/" \
   -H "Authorization: Bearer YOUR_TOKEN" \
   -H "Content-Type: application/json" \
   -d '{
     "book_id": 1,
     "reader_id": 1
   }'
   ```

2. **Возврат книги**:
   ```bash
   curl -X POST "http://localhost:8000/return/1" \
   -H "Authorization: Bearer YOUR_TOKEN"
   ```

### 4. Важные замечания

1. **Ограничения бизнес-логики**:
   - Читатель не может взять больше 3 книг
   - Нельзя выдать книгу, если нет доступных экземпляров
   - Нельзя вернуть книгу, которая не была выдана

2. **Безопасность**:
   - Храните токен в безопасном месте
   - Не передавайте токен через незащищенные каналы
   - Токен действителен 30 минут

3. **Мониторинг**:
   - Логи доступны в консоли
   - Ошибки записываются в файл error.log
   - Статистика доступна через API

### 5. Решение проблем

1. **Ошибка "Token expired"**:
   - Получите новый токен через POST /token

2. **Ошибка "Not enough copies"**:
   - Проверьте количество доступных экземпляров книги

3. **База данных недоступна**:
   - Проверьте наличие файла library.db
   - Убедитесь, что применены миграции

### 6. Полезные команды

1. **Сброс базы данных**:
   ```bash
   rm library.db
   alembic upgrade head
   ```

2. **Просмотр логов**:
   ```bash
   Get-Content -Path .\error.log -Wait
   ```

3. **Остановка сервера**:
   - Нажмите Ctrl+C в консоли


```

## 📝 API Documentation

### Интерактивная документация
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Основные эндпоинты

#### Аутентификация
| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | /register | Регистрация библиотекаря |
| POST | /token | Получение JWT токена |

#### Книги
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | /books | Список книг |
| POST | /books | Добавление книги |
| GET | /books/{id} | Детали книги |
| PUT | /books/{id} | Обновление книги |
| DELETE | /books/{id} | Удаление книги |

## 🔄 Процесс разработки

### Управление версиями
- Используется Git Flow
- Semantic Versioning для релизов
- Автоматические тесты при PR

### Тестирование
- Unit тесты с pytest
- Интеграционные тесты
- 100% покрытие бизнес-логики

## 🎯 Дополнительные возможности

### Система уведомлений (новое)
- Отслеживание сроков возврата
- Email уведомления
- Интеграция с мессенджерами
- Периодические отчеты

### Статистика и аналитика
- Популярные книги
- Активные читатели
- Прогнозирование спроса

## 📈 Масштабирование

### Текущая архитектура поддерживает:
- Горизонтальное масштабирование
- Кэширование запросов
- Асинхронную обработку

## 🤝 Участие в проекте

Этот проект открыт для контрибьюторов! Если вы хотите внести свой вклад:

1. Форкните репозиторий
2. Создайте ветку для ваших изменений
3. Отправьте пулл-реквест

### Связь с автором
- Telegram: @voldemarnif
- Email: vovapilip46@gmail.com

## 📄 Лицензия

Copyright © 2025 Vladimir P.

Этот проект лицензирован под MIT License - подробности в файле [LICENSE](LICENSE)
