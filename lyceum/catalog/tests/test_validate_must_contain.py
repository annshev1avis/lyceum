from django.core.exceptions import ValidationError
from django.test import TestCase

from catalog.validators import ValidateMustContain

__all__ = ["ValidateMustContainTests"]


class ValidateMustContainTests(TestCase):
    def setUp(self):
        self.validator = ValidateMustContain("превосходно", "роскошно")

    def test_positive_1(self):
        self.assertEqual(
            self.validator("превосходно"),
            None,
        )

    def test_positive_2(self):
        self.assertEqual(
            self.validator("роскошно"),
            None,
        )

    def test_positive_with_punctuation(self):
        self.assertEqual(
            self.validator("(роскошно!)..."),
            None,
        )

    def test_positive_several_words(self):
        self.assertEqual(
            self.validator(
                "роскошно написанная книга",
            ),
            None,
        )

    def test_negative_unfinished_word(self):
        with self.assertRaises(ValidationError):
            self.validator("превосходн")

    def test_negative_several_words(self):
        with self.assertRaises(ValidationError):
            self.validator("обычно написанная книга")

    def test_negative_with_punctuation_but_not_word(self):
        with self.assertRaises(ValidationError):
            self.validator("лишнее(роскошно!)...")

    def test_negative_empty_string(self):
        with self.assertRaises(ValidationError):
            self.validator("")

    def test_negative_includes_word_substring_but_not_word(self):
        with self.assertRaises(ValidationError):
            self.validator("нероскошно")

    def test_positive_with_html_tag(self):
        self.assertEqual(
            self.validator("<u>роскошно<u>"),
            None,
        )

    def test_positive_with_html_tag_and_punctuation(self):
        self.assertEqual(
            self.validator("<u>роскошно!)...<u>"),
            None,
        )
