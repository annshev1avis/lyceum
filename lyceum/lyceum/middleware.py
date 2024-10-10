from django.conf import settings


REVERSE_TIME = 10
RUSSIAN_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def reverse_rus_word(word):
    return word[::-1] if word[0].lower() in RUSSIAN_LETTERS else word


class ReverseWordsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.count = 0

    def __call__(self, request):
        self.count += 1

        response = self.get_response(request)

        if settings.ALLOW_REVERSE and self.count % REVERSE_TIME == 0:
            words = response.content.decode().split(" ")
            response.content = " ".join(map(reverse_rus_word, words))
            self.count = 0

        return response
