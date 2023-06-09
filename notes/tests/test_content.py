from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст заметки',
            slug='note-slug', author=cls.author,
        )

    def test_notes_list_for_different_users(self):
        users_bools = (
            (self.author, True),
            (self.reader, False),
        )
        for user, bools in users_bools:
            self.client.force_login(user)
            with self.subTest():
                url = reverse('notes:list')
                response = self.client.get(url)
                object_list = response.context['object_list']
                self.assertEqual((self.note in object_list), bools)

    def test_pages_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', [self.note.slug]),
        )
        for name, args in urls:
            self.client.force_login(self.author)
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                


