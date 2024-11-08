import re

import django.conf

__all__ = ["ReverseWordsMiddleware", "reverse_rus_word"]


REVERSE_TIME = 10
ONLY_RUSSIAN_REGEX = re.compile(r"^\s*[\W_]*[А-Яа-яЁё]+[\W_]*\s*$")


def reverse_rus_word(word):
    if word == "":
        return word

    return word[::-1] if ONLY_RUSSIAN_REGEX.match(word) else word


class ReverseWordsMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def check_should_reverse(cls):
        if django.conf.settings.ALLOW_REVERSE not in (True, None):
            return False

        cls.count += 1
        if cls.count == 10:
            cls.count = 0
            return True

        return False

    def __call__(self, request):
        response = self.get_response(request)

        if not self.check_should_reverse():
            return response

        words = response.content.decode("utf-8").split()
        response.content = " ".join(map(reverse_rus_word, words)).encode(
            "utf-8",
        )

        return response
