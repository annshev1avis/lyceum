from django.conf import settings


REVERSE_TIME = 10
RUSSIAN_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def reverse_rus_word(word):
    if word == "":
        return word
    return word[::-1] if word[0].lower() in RUSSIAN_LETTERS else word


class ReverseWordsMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ReverseWordsMiddleware.count += 1

        response = self.get_response(request)

        if (
            settings.ALLOW_REVERSE or settings.ALLOW_REVERSE is None
        ) and ReverseWordsMiddleware.count % REVERSE_TIME == 0:
            words = response.content.decode().split()
            response.content = " ".join(map(reverse_rus_word, words))
            ReverseWordsMiddleware.count = 0

        return response
