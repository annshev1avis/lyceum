import django.test
from django.urls import reverse


__all__ = ["ReverseWordsMiddlewareTest"]


class ReverseWordsMiddlewareTest(django.test.TestCase):

    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_reverse_coffee_endpoint(self):
        client = django.test.Client()
        results = []
        for _ in range(10):
            response = client.get("/coffee/")
            results.append(response.content.decode())

        self.assertEqual(results.count("Я кинйач"), 1)

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_disable_reversing(self):
        client = django.test.Client()
        results = []
        for _ in range(10):
            response = client.get("/coffee/")
            results.append(response.content.decode())

        self.assertEqual(
            results.count("Я кинйач"),
            0,
            "Не сработало отключение ReverseWordsMiddleware",
        )

    @django.test.override_settings(ALLOW_REVERSE=None)
    def test_reverse_coffee_endpoint_default(self):
        client = django.test.Client()
        results = []
        for _ in range(10):
            response = client.get("/coffee/")
            results.append(response.content.decode())

        self.assertEqual(results.count("Я кинйач"), 1)

    def test_crazy(self):
        form_data = {
            "text": (
                "Привет, этo почтi-почти Pуcский текст@, просто≈ "
                "Как-то со спецü символами:) ¡сорри∑! Hу ещё раз ¡сорри! "
                "Ёжика не видели?"
            ),
        }

        results = []
        for _ in range(10):
            response = django.test.Client().post(
                reverse("homepage:echo_submit"),
                data=form_data,
            )
            results.append(response.content)

        expected_text = (
            "тевирП, этo почтi-итчоп Pуcский тскет@, "
            "отсорп≈ каК-от ос спецü ималовмис:) ¡иррос∑! "
            "Hу ёще зар ¡иррос! акижЁ ен иледив?"
        ).encode("utf-8")

        self.assertIn(expected_text, results)
