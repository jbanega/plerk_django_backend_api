from django.test import SimpleTestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):

    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "index.html")

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "plerk RESTful API")

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
        self.response, "This should not be on the homepage.")


class ResponsePageTests(SimpleTestCase):

    def setUp(self):
        url = reverse("response")
        self.response = self.client.get(url)

    def test_responsehome_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_template(self):
        self.assertTemplateUsed(self.response, "response.html")

    def test_response_contains_correct_html(self):
        self.assertContains(self.response, "J")