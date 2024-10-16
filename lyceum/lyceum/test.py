import django.test


class ReverseWordsMiddlewareTest(django.test.TestCase):

    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_reverse_coffee_endpoint(self):
        client = django.test.Client()
        results = []
        for i in range(10):
            response = client.get("/coffee/")
            results.append(response.content.decode())
        self.assertEqual(results.count("Я кинйач"), 1)

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_disable_reversing(self):
        client = django.test.Client()
        results = []
        for i in range(10):
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
        for i in range(10):
            response = client.get("/coffee/")
            results.append(response.content.decode())
        self.assertEqual(results.count("Я кинйач"), 1)
