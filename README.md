# homework_bot

### Описание:
Данный telegram bot предназначен для работы через интерфейс API сервиса Яндекс Практикум.
В задачи бота входит определение стадии проверки домашнего задания студента ЯП с указанным интервалом и отправка сообщения с полученными данными студенту в чат мессенджера telegram. 

### Используемые технологии и библиотеки:
- Python
- Python-telegam-bot

### Описание обязательных переменных:
- PRACTICUM_TOKEN - токен для проверки домашки Практикума
- TELEGRAM_TOKEN - токен телеграм-бота
- TELEGRAM_CHAT_ID - чат для отправки сообщения

### Описание функций:
- Функция check_tokens() проверяет доступность переменных окружения, которые необходимы для работы программы.
- Функция get_api_answer() делает запрос к единственному эндпоинту API-сервиса. В качестве параметра в функцию передается временная метка. В случае успешного запроса должна вернуть ответ API, приведя его из формата JSON к типам данных Python.
- Функция check_response() проверяет ответ API на соответствие документации API сервиса ЯП. В качестве параметра функция получает ответ API, приведенный к типам данных Python.
- Функция parse_status() извлекает из информации о конкретной домашней работе статус этой работы. В качестве параметра функция получает только один элемент из списка домашних работ. В случае успеха, функция возвращает подготовленную для отправки в Telegram строку, содержащую один из вердиктов словаря HOMEWORK_VERDICTS
- Функция send_message() отправляет сообщение в Telegram чат, определяемый переменной окружения TELEGRAM_CHAT_ID. Принимает на вход два параметра: экземпляр класса Bot и строку с текстом сообщения.

### Регистрация бота в telegram:
1. В Телеграме найти бота @BotFather
2. Ввести команду /newbot
3. Следуя подсказкам придумать название бота и логин для него.
4. Получить ссылку на нового бота и API токен.
5. Ввести команду /mybots
6. Выбрать своего бота и нажать Edit Bot
7. Добавить информацию description, about, botpic, commands

###  Запуск бота на персональном компьютере:
1. Клонируйте репозиторий:
```
git clone git@github.com:pirut2/homework_bot.git
```

Создайте и активируйте виртуальное окружение

```
python -m venv venv
```

```
source venv/scripts/activate
```

Обновите pip:

```
python -m pip install --upgrade pip
```

Установите зависимости из requirements.txt:

```
pip install -r requirements.txt
```
Создайте в корневой директории файл .env и пропишите в него необходимые для работы переменные.

Запустите telegram bot:

```
python homework.py
```





  
