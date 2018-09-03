from django.conf import settings

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)
        # to set a cookie we need to first visit the domain.
        # 404 pages load the quickest!
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/'
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session('edith@example.com')

        # She goes to the home page and starts a lit
        self.browser.get(self.live_server_url)
        self.add_cargo_item('Oil')
        self.add_cargo_item('Barley')
        first_cargo_url = self.browser.current_url

        # She notices a "My cargo shipments" link, for the first time.
        self.browser.find_element_by_link_text('My cargo shipments').click()

        # She sees that her cargo list is there, named according to its
        # first cargo item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Oil')
        )
        self.browser.find_element_by_link_text('Oil').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_cargo_url)
        )

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_cargo_item('Grain')
        second_cargo_url = self.browser.current_url

        # Under "My cargo shipments", her new cargo list appears
        self.browser.find_element_by_link_text('My cargo shipments').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Grain')
        )
        self.browser.find_element_by_link_text('Grain').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_cargo_url)
        )

        # She logs out. The "My cargo shipments" option disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My cargo shipments'),
            []
        ))
