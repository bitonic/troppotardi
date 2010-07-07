from troppotardi.tests import *

class TestImagesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='images', action='index'))
        # Test response...
