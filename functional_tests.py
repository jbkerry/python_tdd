#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('cargo_list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Roger has heard about a cool new fantasy trade game. He goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention cargo
        self.assertIn('Cargo', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Cargo', header_text)

        # He is invited to enter a type of cargo
        inputbox = self.browser.find_element_by_id('new_cargo')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a cargo type'
        )

        # He types "Grain" into a text box
        inputbox.send_keys('Grain')

        # When he hits enter, the page updates, and now the page lists "1: Grain" as an item of cargo
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Grain')

        # There is still a text box inviting him to add another type of cargo. He enters "Iron".
        inputbox = self.browser.find_element_by_id('new_cargo')
        inputbox.send_keys('Iron')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both types of cargo on his list
        self.check_for_row_in_list_table('1: Grain')
        self.check_for_row_in_list_table('2: Iron')

        # Roger wonders whether the site will remember his list. Then he sees that the site has generated a unique URL
        # for him -- there is some explanatory text to that effect.
        self.fail('Finish the test!')

        # He visits that URL - his cargo list is still there.

        # Satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')

