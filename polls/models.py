from datetime import timedelta
from functools import cached_property
from itertools import count

from django.db import models

from django.utils import timezone

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
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class QuestionQuerySet(models.QuerySet):
    def by_category(self, slug):
        if slug and slug != "all":
            return self.filter(category__slug=slug)
        
        return self

    def sorted_by(self, option):
        return self.order_by(option or "-pub_date")

    def community_polls(self, user):
        qs = self.exclude(creator=user)
        if user.is_authenticated:
            qs = qs.exclude(id__in=user.polls_voted.all())

        return qs

    def user_polls(self, user):
        if user.is_authenticated:
            return self.filter(creator=user)
        
        return self.none()
    

class Questions(models.Model):
    objects = QuestionQuerySet.as_manager()
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE)
    creator = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="polls_create",
        null=True,
    )
    views_count = models.IntegerField(default=0, null=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timedelta(minutes=30)
    
    @cached_property
    def total_votes(self):
        return self.choice_set.aggregate(models.Sum("votes"))["votes__sum"] or 0

    def similar_polls(self, user):
        qs = self.__class__.objects.filter(category=self.category).exclude(id=self.id)
        if user.is_authenticated:
            qs = qs.exclude(id__in=user.polls_voted.all())
        
        return qs.order_by("-pub_date")[:4]

    def increment_views(self, session):
        session_key = f"viewed_{self.id}"

        if not session.get(session_key):
            self.__class__.objects.filter(pk=self.pk).update(views_count=models.F("views_count") + 1)
            session[session_key] = True
            return True
        
        return False

    def vote(self, user, choice):
        from django.db import transaction
        with transaction.atomic():
            choice.votes = models.F('votes') + 1
            choice.save()

            user.votes = models.F('votes') + 1
            user.save()

            user.polls_voted.add(self)

    def __str__(self):
        return self.question_text

    class Meta:
        db_table = "questions"
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Choice(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        db_table = "choices"
        verbose_name = "choice"
        verbose_name_plural = "choices"
