class BaseErorr(Exception):
    """Базовый класс ошибки."""

    pass


class ResponseError(BaseErorr):
    """Статус ответа на API запрос не равен 200."""

    def __init__(self, msg, code):
        """Конструктор."""
        self.msg = msg
        self.code = code


class PageError(BaseErorr):
    """Что то не так."""

    pass


class HomeworksNameKeyError(BaseErorr):
    """Ключ homework_name отсутствует в ответе API."""

    pass


class MessageError(BaseErorr):
    """Ошибка в отправке сообщения."""

    pass


class TokenError(BaseErorr):
    """Ошибка в проверке токенов."""

    pass


class CheckTokensError(BaseErorr):
    """Check tokens."""

    pass
