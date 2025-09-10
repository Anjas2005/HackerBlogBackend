from django.db import models

# Create your models here.

class BestNews(models.Model):
    Rank=models.IntegerField(primary_key=True)
    Title=models.CharField(max_length=500)
    Link_To_Article=models.URLField(max_length=500)
    Points=models.CharField(max_length=100)
    Author=models.CharField(max_length=100)
    Post_Time=models.CharField(max_length=100)
    Scraped_Page_Link=models.URLField(max_length=500)