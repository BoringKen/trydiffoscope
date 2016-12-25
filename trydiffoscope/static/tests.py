from trydiffoscope.utils.test import TestCase

class SmokeTest(TestCase):
    def test_terms(self):
        self.assertGET(200, 'static:terms')

    def test_privacy(self):
        self.assertGET(200, 'static:privacy')
