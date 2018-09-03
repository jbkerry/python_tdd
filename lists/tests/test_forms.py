import unittest
from unittest.mock import patch, Mock
from django.test import TestCase

from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm, NewListForm
)
from lists.models import Item, List


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a cargo type"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_item(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])


class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        cargo_list = List.objects.create()
        form = ExistingListItemForm(for_list=cargo_list)
        self.assertIn('placeholder="Enter a cargo type', form.as_p())

    def test_form_validation_for_blank_items(self):
        cargo_list = List.objects.create()
        form = ExistingListItemForm(for_list=cargo_list, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        cargo_list = List.objects.create()
        Item.objects.create(list=cargo_list, text='Maize')
        form = ExistingListItemForm(for_list=cargo_list, data={'text': 'Maize'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        cargo_list = List.objects.create()
        form = ExistingListItemForm(for_list=cargo_list, data={'text': 'Lumber'})
        new_cargo = form.save()
        self.assertEqual(new_cargo, Item.objects.all()[0])


class NewListFormTest(unittest.TestCase):

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(
        self, mock_List_create_new
    ):
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='new item text'
        )

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_with_owner_if_user_authenticated(
        self, mock_List_create_new
    ):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='new item text', owner=user
        )

    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_object(self, mock_List_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_List_create_new.return_value)
