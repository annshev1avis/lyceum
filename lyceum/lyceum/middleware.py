import re

import django.conf

__all__ = ["ReverseWordsMiddleware", "reverse_rus_word"]


REVERSE_TIME = 10

RUS_WORD = re.compile(r"\b[а-яА-ЯёЁ]+\b")


def reverse_rus_word(word):
    if word == "":
        return word

    match = RUS_WORD.search(word)

    if match:
        return (
            word[: match.start()] + match.group()[::-1] + word[match.end() :]
        )

    return word


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

        words = response.content.decode("utf-8").split()
        response.content = " ".join(map(reverse_rus_word, words)).encode(
            "utf-8",
        )

        return response
