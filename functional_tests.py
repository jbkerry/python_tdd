#!/usr/bin/env python

from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Roger has heard about a cool new fantasy trade game. He goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention cargo
        self.assertIn('Cargo', self.browser.title)
        self.fail('Finish the test!')

        # He is invited to enter a type of cargo

        # He types "Grain" into a text box

        # When he hits enter, the page updates, and now the page lists "Carriage 1: Grain" as an item of cargo

        # There is still a text box inviting him to add another type of cargo. He enters "Iron".

        # The page updates again, and now shows both types of cargo on his list

        # Roger wonders whether the site will remember his list. Then he sees that the site has generated a unique URL
        # for him -- there is some explanatory text to that effect.

        # He visits that URL - his cargo list is still there.

        # Satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')

