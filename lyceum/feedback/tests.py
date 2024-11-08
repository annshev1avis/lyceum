from django.test import Client, TestCase
from django.urls import reverse
from parameterized import parameterized

import feedback.forms


__all__ = []


class FormTests(TestCase):
    def setUp(self):
        self.form = feedback.forms.FeedbackForm()

    @parameterized.expand(
        [
            ("name", "Название"),
            ("text", "Текст фидбека"),
            ("mail", "Электронная почта"),
        ],
    )
    def test_field_label(self, field, expected_label):
        field_label = self.form.fields[field].label
        self.assertEqual(field_label, expected_label)

    @parameterized.expand(
        [
            ("name", "О чем ваш фидбек"),
            ("text", "Поделитесь впечатлениями"),
            ("mail", "Введите электронную почту"),
        ],
    )
    def test_field_help_text(self, field, expected_help_text):
        field_help_text = self.form.fields[field].help_text
        self.assertEqual(field_help_text, expected_help_text)

    def test_form_is_in_context(self):
        response = Client().get(reverse("feedback:feedback"))
        self.assertIn("form", response.context)

    def test_form_in_context_type(self):
        response = Client().get(reverse("feedback:feedback"))
        self.assertIsInstance(
            response.context["form"],
            feedback.forms.FeedbackForm,
        )

    def test_redirects(self):
        form_data = {
            "name": "test_name",
            "text": "test_text",
            "mail": "test@email.com",
        }
        response = Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse("feedback:feedback"))

    def test_form_name_is_not_requered(self):
        form = feedback.forms.FeedbackForm(
            {
                "text": "test_text",
                "mail": "test@email.com",
            },
        )
        self.assertFormError(form, "name", [])

    def test_form_validate_email(self):
        form = feedback.forms.FeedbackForm(
            {
                "name": "test_name",
                "text": "test_text",
                "mail": "bad_email",
            },
        )
        self.assertFormError(form, "mail", "Enter a valid email address.")
