# books/tests/test_models.py
from django.test import TestCase
from books.models import Book, Category
from django.contrib.auth.models import User

class BookModelTest(TestCase):
    def setUp(self):
        # Create required dependencies
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Fiction')

    def test_book_creation(self):
        # Include ALL non-nullable fields
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            category=self.category,
            price=19.99,  # <-- REQUIRED FIELD
            uploaded_by=self.user,
            file="test.pdf"  # <-- REQUIRED FIELD
        )
        self.assertEqual(str(book), "Test Book")