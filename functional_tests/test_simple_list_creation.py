#!/usr/bin/env python

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # Roger has heard about a cool new fantasy trade game. He goes to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention cargo
        self.assertIn('Cargo', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Cargo', header_text)

        # He is invited to enter a type of cargo
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a cargo type'
        )

        # He types "Grain" into a text box
        inputbox.send_keys('Grain')

        # When he hits enter, the page updates, and now the page lists "1: Grain" as an item of cargo
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Grain')

        # There is still a text box inviting him to add another type of cargo. He enters "Iron".
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Iron')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both types of cargo on his list
        self.wait_for_row_in_list_table('1: Grain')
        self.wait_for_row_in_list_table('2: Iron')

        # Satisfied, he goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Roger starts a new cargo list
        self.browser.get(self.live_server_url)
        self.add_cargo_item('Grain')

        # He notices that his list has a unique URL
        roger_list_url = self.browser.current_url
        self.assertRegex(roger_list_url, '/lists/.+')

        # Now a new user, Billy, comes along to the site.

        # # We use a new browser session to make sure that no information of Roger's is coming through from cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Billy visits the home page. There is no sign of Roger's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Grain', page_text)
        self.assertNotIn('Iron', page_text)

        # Billy starts a new list by entering a new item. He trades different cargo to Roger...
        self.add_cargo_item('Timber')

        # Billy gets his own unique URL
        billy_list_url = self.browser.current_url
        self.assertRegex(billy_list_url, '/lists/.+')
        self.assertNotEqual(billy_list_url,roger_list_url)

        # Again, there is no trace of Roger's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Grain', page_text)
        self.assertIn('Timber', page_text)

        # Satisfied they both go back to sleep
