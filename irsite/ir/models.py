from django.db import models


# Create your models here.
class Keyword(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    keyword = models.CharField(max_length=10)

    def __str__(self):
        return self.keyword


class Abstract(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    abstract = models.TextField()
    author = models.CharField(max_length=10)
    publisher = models.CharField(max_length=30)
    keywords = models.ManyToManyField(Keyword)

    def __str__(self):
        return self.abstract
