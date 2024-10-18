from functools import wraps
import re

from django.core.exceptions import ValidationError


def is_int_1_32767(value):
    if not 1 <= value <= 32767:
        raise ValidationError(
            "Число должно быть целым и принадлежать промежутку от 1 до 32767",
        )


def ValidateMustContain(*words):

    @wraps(ValidateMustContain)
    def validator(text):
        nonlocal words

        text = " " + text + " "

        regex = r" [^\da-zа-я]*(?:" + "|".join(words) + r")[^\da-zа-я]* "
        necessary_words = re.findall(
            regex,
            text,
            re.IGNORECASE,
        )

        if not necessary_words:
            necessary_words_for_exception_text = "/".join(
                map(lambda w: f"'{w}'", words),
            )

            raise ValidationError(
                "Строка должна содержать одно из слов ",
                f"{necessary_words_for_exception_text}",
            )

    return validator
