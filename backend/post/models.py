from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    newslink=models.CharField(max_length=200)
    category=models.CharField(max_length=50)
    keyword=models.CharField(max_length=100)


    def __str__(self):
        return self.title