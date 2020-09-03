from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    newslink=models.CharField(max_length=200)
    category=models.CharField(max_length=50)
    keyword=models.CharField(max_length=100)
    press=models.CharField(max_length=10) #언론사
    #time=models.DateTimeField(null=True)
    #view_count=models.IntegerField(default=0)
    news_num = models.IntegerField()

    def __str__(self):
        return self.title

