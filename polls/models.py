from datetime import timedelta

from django.utils import timezone
from django.db import models

from app import settings

class Categories(models.Model):
    category_name = models.CharField(
        max_length=50, default="", verbose_name="Category Name"
    )
    slug = models.SlugField(
        max_length=100, unique=True, blank=True, null=True, verbose_name="URL"
    )
    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



class Questions(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE)
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='polls_create', null=True)
    views_count = models.IntegerField(default=0, null=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timedelta(minutes=30)

    def __str__(self):
        return self.question_text
    
    class Meta:
        db_table = 'questions'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'



class Choice(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
    
    class Meta:
        db_table = 'choices'
        verbose_name = 'choice'
        verbose_name_plural = 'choices'