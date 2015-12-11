from trydiffoscope.utils.test import TestCase

class SmokeTest(TestCase):
    def test_view(self):
        self.assertGET(200, 'compare:view')
