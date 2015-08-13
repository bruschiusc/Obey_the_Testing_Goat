from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http.request import HttpRequest
from django.template.loader import render_to_string


# Create your tests here.
class HomePageTest (TestCase):
    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        
    def test_home_page_return_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        #self.assertTrue(response.content.startswith(b'<html>'))
        #self.assertIn(b'<title>To-Do lists</title>', response.content)
        #elf.assertTrue(response.content.endswith(b'</html>'))
        expect_html = render_to_string('home.html')
        self.assertEqual(response.content.decore(), expect_html)