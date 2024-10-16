import http

import django.test


class HomepageTests(django.test.TestCase):
    def test_homepage_endpoint(self):
        response = django.test.Client().get("/")
        self.assertEqual(response.status_code, 200)
        str_content = str(response.content, encoding="utf-8")
        self.assertEqual(str_content, "Главная")

    def test_teapot_endpoint(self):
        response = django.test.Client().get("/coffee/")
        self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)
        str_content = str(response.content, encoding="utf-8")
        self.assertEqual(str_content, "Я чайник")
