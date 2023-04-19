

class ResponseError(Exception):
    """Статус ответа на API запрос не равен 200."""

    pass


class PageError(Exception):
    """Что то не так."""

    pass


class HomeworksNameKeyError(Exception):
    """Ключ homework_name отсутствует в ответе API."""

    pass


class MessageError(Exception):
    """Ошибка в отправке сообщения."""

    pass


class TokenError(Exception):
    """Ошибка в проверке токенов."""

    pass
