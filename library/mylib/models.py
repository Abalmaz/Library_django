from django.db import models

# Create your models here.


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name


class PublishingHouse(Timestamp):
    name = models.CharField(max_length=35)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Author(Timestamp):
    first_name = models.CharField(max_length=25)
    second_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, blank=True)
    pseudonym = models.CharField(max_length=25, blank=True)
    birth_date = models.DateField()
    death_date = models.DateField(blank=True, null=True)
    biography = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return self.second_name

    @property
    def full_name(self):
        return '%s %s %s' % (self.first_name, self.middle_name, self.second_name)

    def short_name(self):
        if self.pseudonym:
            return '{}'.format(self.pseudonym)
        elif self.middle_name:
            return '{} {}. {}.'.format(self.second_name, self.first_name[0].capitalize(), self.middle_name[0].capitalize())
        else:
            return '{} {}.'.format(self.second_name, self.first_name[0].capitalize())

    class Meta:
        ordering = ('second_name',)


class Book(Timestamp):
    title = models.CharField(unique=True, max_length=80)
    year = models.IntegerField()
    number_page = models.IntegerField()
    publishing = models.ForeignKey(PublishingHouse, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, through='BookAuthor')
    genre = models.ManyToManyField(Genre)
    description = models.TextField()
    cover = models.ImageField(blank=True)

    def __str__(self):
        return self.title


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        auto_created = True

