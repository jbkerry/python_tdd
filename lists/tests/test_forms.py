from django.test import TestCase

from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm
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

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)


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
