from datetime import timedelta
from functools import cached_property

from django.db import models, transaction
from django.utils import timezone

from django.conf import settings


class Category(models.Model):
    category_name = models.CharField(
        max_length=50, default="", verbose_name="Category Name"
    )
    slug = models.SlugField(
        max_length=100, unique=True, blank=True, null=True, verbose_name="URL"
    )

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class QuestionQuerySet(models.QuerySet):
    """
    Custom QuerySet for Question model providing chainable filter methods
    for categories, sorting, and user-specific poll visibility.
    """

    def by_category(self, slug):
        """Filter questions by category slug if provided and not 'all'."""

        if slug and slug != "all":
            return self.filter(category__slug=slug)
        
        return self

    def sorted_by(self, option):
        """Order questions by the given option or fallback to newest first."""

        return self.order_by(option or "-pub_date")

    def community_polls(self, user):
        """
        Return polls from the community: excludes polls created by the user
        and polls the user has already voted in.
        """

        qs = self
        if user.is_authenticated:
            qs = qs.exclude(id__in=user.polls_voted.all()).exclude(creator=user)

        return qs

    def user_polls(self, user):
        """Return only the polls created by the specified user."""

        if user.is_authenticated:
            return self.filter(creator=user)
        
        return self.none()
    

class Question(models.Model):
    objects = QuestionQuerySet.as_manager() # connecting methods
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    views_count = models.IntegerField(default=0, null=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timedelta(minutes=30)
    

    def voted_ids(user) -> set:
        if user.is_authenticated:
            return set(user.polls_voted.values_list("id", flat=True))
        
        return set()

    # function with a cache decorator, to be called in a template
    @cached_property
    def total_votes(self):
        # return the sum of votes in the choice_set list
        return self.choice_set.aggregate(models.Sum("votes"))["votes__sum"] or 0

    def similar_polls(self, user):
        # filter by category excluding the current poll to avoid repetition
        qs = self.__class__.objects.filter(category=self.category).exclude(id=self.id)
        if user.is_authenticated:
            # if the user is authenticated, we exclude the polls for which he voted.
            qs = qs.exclude(id__in=user.polls_voted.all())
        
        return qs.order_by("-pub_date")[:4]

    def increment_views(self, session):
        session_key = f"viewed_{self.id}"

        # if there are no views of this poll in the user's session, add +1 to the views_count field
        if not session.get(session_key):
            self.__class__.objects.filter(pk=self.pk).update(views_count=models.F("views_count") + 1)
            self.refresh_from_db(fields=['views_count'])
            session[session_key] = True
            return True
        
        return False

    # we use the atomic decorator for the function to avoid data loss.
    @transaction.atomic
    def vote(self, poll_id, user, choice) -> bool:
        if not poll_id in user.polls_voted.values_list("id", flat=True):
            choice.votes = models.F('votes') + 1
            choice.save()

            user.votes = models.F('votes') + 1
            user.save()
            user.polls_voted.add(self)

            return True
        
        return False

    def __str__(self):
        return self.question_text

    class Meta:
        db_table = "question"
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        db_table = "choices"
        verbose_name = "choice"
        verbose_name_plural = "choices"
