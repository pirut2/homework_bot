import logging
import os
import requests
import exceptions
import time
import telegram
from dotenv import load_dotenv
from http import HTTPStatus

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TOKEN_NAMES = ('PRACTICUM_TOKEN', 'TELEGRAM_CHAT_ID', 'TELEGRAM_TOKEN')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def check_tokens():
    """Проверка токенов."""
    logging.debug('Проверка доступности переменных окружения')
    for name in TOKEN_NAMES:
        if not globals()[name]:
            logging.critical(f'Проблемы с токеном {name}', exc_info=True)
            raise exceptions.CheckTokensError
        return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def send_message(bot, message):
    """Отправка сообщения."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
        logging.debug(f'Сообщение {message} отправлено.', exc_info=True)
    except telegram.error.TelegramError as error:
        logging.error(f'Ошибка в отправке сообщения {error}', exc_info=True)
        raise exceptions.MessageError(f'Ошибка в отправке сообщения {error}')


def get_api_answer(timestamp):
    """Запрос к эндпоинту, приводит формат JSON к данным Python."""
    url = ENDPOINT
    headers = HEADERS
    payload = {'from_date': timestamp}
    try:
        answer = requests.get(url, headers=headers, params=payload)
    except requests.exceptions.RequestException:
        logging.error('Проблема с доступом к Endpoint.', exc_info=True)
    finally:
        if answer.status_code != HTTPStatus.OK:
            logging.error('Статус запроса к API  не соответствует 200.',
                          exc_info=True)
            raise exceptions.ResponseError(
                f'Ошибка запроса: {answer.status_code}',
                HTTPStatus.CONFLICT
            )
        else:
            response = answer.json()
        return response


def check_response(response):
    """Проверка запроса API."""
    if not isinstance(response, dict):
        logging.error('Ответ API не является словарем.', exc_info=True)
        raise TypeError('Ответ API не является словарем.')
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        logging.error('homeworks не является списком.', exc_info=True)
        raise TypeError('homeworks не является списком.')
    if 'homeworks' not in response:
        logging.error('Ключа homeworks нет в ответе API.', exc_info=True)
        raise KeyError('Ключа homeworks нет в ответе API.')
    return homeworks


def parse_status(homework):
    """Проверка статуса домашней работы."""
    if 'homework_name' not in homework:
        logging.error('Отсутствует homework_name', exc_info=True)
        raise exceptions.HomeworksNameKeyError
    try:
        verdict = HOMEWORK_VERDICTS[homework.get('status')]
        homework_name = homework.get('homework_name')
    except KeyError:
        logging.critical('Ошибка в значении ключа.', exc_info=True)
    except TypeError:
        logging.critical('Ошибка в значении типа.', exc_info=True)
    except SyntaxError:
        logging.critical('Синтаксическая ошибка.', exc_info=True)
    except Exception as erorr:
        logging.error(f'Неожиданная ошибка {erorr}'
                      'при запросе статуса домашней работы.', exc_info=True)
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if check_tokens() is not True:
        logging.critical('Ошибка в обработке токенов', exc_info=True)
        return

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    while True:
        try:
            old_status = ''
            api_request = get_api_answer(timestamp)
            timestamp = api_request.get('current_date')
            check_homework = check_response(api_request)
            if check_homework:
                status = parse_status(check_homework[0])
                if status != old_status:
                    send_message(bot, message=status)
                    status = old_status
                    logging.info('Новое сообщение у бота.')
                else:
                    logging.info('Ничего нового в статусе домашней работы.')
            else:
                logging.info('Статус не изменился.')
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.critical(message, exc_info=True)
            raise exceptions.BaseErorr('Большие проблемы в main.')
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
