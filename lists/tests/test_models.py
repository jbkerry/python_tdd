#!/usr/bin/env python

from lists.models import Item, List
from django.test import TestCase
from django.core.exceptions import ValidationError


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        cargo_list = List.objects.create()
        item = Item()
        item.list = cargo_list
        item.save()
        self.assertIn(item, cargo_list.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        cargo_list = List.objects.create()
        Item.objects.create(list=cargo_list, text='Blah')
        with self.assertRaises(ValidationError):
            item = Item(list=cargo_list, text='Blah')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='Blah')
        item = Item(list=list2, text='Blah')
        item.full_clean() # should not raise

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        cargo_list = List.objects.create()
        self.assertEqual(cargo_list.get_absolute_url(), f'/lists/{cargo_list.id}/')
