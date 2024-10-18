import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def is_int_1_32767(value):
    if not 1 <= value <= 32767:
        raise ValidationError(
            "Число должно быть целым и принадлежать промежутку от 1 до 32767",
        )


@deconstructible
class ValidateMustContain:
    def __init__(self, *words):
        self.words = words
        self.regex = r" [^\da-zа-я]*(?:" + "|".join(words) + r")[^\da-zа-я]* "

    def __call__(self, text):
        text = " " + text + " "

        necessary_words = re.findall(
            self.regex,
            text,
            re.IGNORECASE,
        )

        if not necessary_words:
            necessary_words_for_exception_text = (
                "/".join(f"'{w}'" for w in self.words),
            )

            raise ValidationError(
                "Строка должна содержать одно из слов ",
                f"{necessary_words_for_exception_text}",
            )

    def __eq__(self, other):
        return set(self.words) == set(other.words)