import re

import django.conf

__all__ = ["ReverseWordsMiddleware"]


REVERSE_TIME = 10

RUSSIAN_WORD = re.compile(r"\b[а-яА-ЯёЁ]+\b")


class ReverseWordsMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def check_should_reverse(cls):
        if django.conf.settings.ALLOW_REVERSE not in (True, None):
            return False

        cls.count += 1
        if cls.count == REVERSE_TIME:
            cls.count = 0
            return True

        return False

    def __call__(self, request):
        response = self.get_response(request)

        if not self.check_should_reverse():
            return response

        response.content = self.reverse_russian_words(
            response.content.decode(),
        ).encode()

        return response

    @staticmethod
    def reverse_russian_words(str_content):
        return RUSSIAN_WORD.sub(lambda m: m.group()[::-1], str_content)
