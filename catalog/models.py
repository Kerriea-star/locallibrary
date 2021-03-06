import uuid # Required for unique book instances.
from django.db import models
from django.urls import reverse

class Genre(models.Model):
    # Model representing a book genre
    name = models.CharField(max_length=200, help_text='Enter a book genre e.g.(a science fiction)')

    def __str__(self):
        """String for representing the model object."""
        return self.name

class Book(models.Model):
    """Model representing a book but not a specific copy of book."""
    title = models.CharField(max_length=200)
    #Foreign key used because book can only have one author but authors can have multiple books.
    #Author as a string than as an objects because it hasn't been declared
    author = models.ForeignKey('Author', on_delete=models.SET_NUT, null=True) 
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book.')
    isbn = models.CharField('ISBN', max_length=13, unique=True
                           help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    # ManytoManyField used because genres can contain many books. Books can cover many geners.
    # Genre class is already defined so we can specify the object above.
    genre = models.ManytoManyField(Genre, help_text='Select a genre for this book.')

    def __str__(self):
        # String for representing the model object.
        return self.title

    def get_absolute_url(self):
        # Returns a detail url to access the record for this book.
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """Model representing a specific copy of a book i.e.(that can be copied from a library.)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique id for this particular book in the whole library.')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', Maitenance),
        ('o', On loan),
        ('a', Available),
        ('r', reserved),
    )        

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m'
        help_text='Book availability.'
    )

    class meta:
        ordering = ('due_back')

    def __str__(self):
        """String for representing the model object.""" 
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class meta:
        ordering = ('first_name', 'last_name')

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """string representing the model object."""
        return f'{self.last_name}, {self.first_name}'        