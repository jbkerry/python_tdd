#!/usr/bin/env python

from lists.models import Item, List
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


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

    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        new_cargo = List.objects.first()
        self.assertEqual(new_cargo.owner, user)

    def test_lists_can_have_owners(self):
        List(owner=User())  # should not raise

    def test_list_owner_is_optional(self):
        List().full_clean()  # should not raise

    def test_create_returns_new_list(self):
        returned = List.create_new(first_item_text='new item text')
        new_cargo = List.objects.first()
        self.assertEqual(returned, new_cargo)

    def test_list_name_is_first_item_text(self):
        cargo_list = List.objects.create()
        Item.objects.create(list=cargo_list, text='first item')
        Item.objects.create(list=cargo_list, text='second item')
        self.assertEqual(cargo_list.name, 'first item')

    def test_list_can_add_a_user_to_share(self):
        cargo_list = List.objects.create()
        shared_user = User.objects.create(email='an@example.com')
        cargo_list.shared_with.add('an@example.com')
        self.assertIn(shared_user, cargo_list.shared_with.all())
