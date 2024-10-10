from django.test import Client, override_settings, TestCase


class ReverseWordsMiddlewareTest(TestCase):

    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_coffee_endpoint(self):
        client = Client()
        for i in range(9):
            response = client.get("/coffee/")
            self.assertEqual(response.content.decode(), "Я чайник")

        response = client.get("/coffee/")
        self.assertEqual(response.content.decode(), "Я кинйач")

    @override_settings(ALLOW_REVERSE=False)
    def test_disable_reversing(self):
        client = Client()

        for i in range(10):
            response = client.get("/coffee/")
            self.assertEqual(
                response.content.decode(),
                "Я чайник",
                "Не сработало отключение ReverseWordsMiddleware",
            )

    @override_settings(ALLOW_REVERSE=None)
    def test_default_reversing_enabled(self):
        client = Client()
        for i in range(9):
            response = client.get("/coffee/")
            self.assertEqual(response.content.decode(), "Я чайник")

        response = client.get("/coffee/")
        self.assertEqual(response.content.decode(), "Я кинйач")
