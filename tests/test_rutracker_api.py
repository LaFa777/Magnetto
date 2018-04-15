import unittest
import magnetto
from magnetto import (RutrackerApi, MagnettoCaptchaError,
                      MagnettoIncorrectСredentials)

magnetto.RUTRACKER_URL = "http://localhost:9877/rutracker/"


class TestRutrackerApi(unittest.TestCase):

    def setUp(self):
        self.api = RutrackerApi()
        try:
            self.api.authorization("good", "1234")
        except MagnettoCaptchaError:
            self.api.authorization("good", "1234", "1234")

    def test_authorization(self):
        api = RutrackerApi()

        with self.assertRaises(MagnettoCaptchaError):
            api.authorization("good", "1234")

        try:
            api.authorization("good", "1234")
        except MagnettoCaptchaError as err:
            self.assertEqual(
                err.url, '//static.t-ru.org/captcha/to_captcha.jpg')

        api.authorization("good", "1234", "1234")
        self.assertTrue(api.is_logged())

        last = api.get_last_request_data()
        self.assertEqual(last['url'], magnetto.RUTRACKER_URL + "index.php")

        api = RutrackerApi()
        with self.assertRaises(MagnettoIncorrectСredentials):
            try:
                api.authorization("bad", "bad")
            except MagnettoCaptchaError:
                api.authorization("bad", "bad", "1234")
