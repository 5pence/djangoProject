from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    """
    The first manager declared in a model becomes the default manager.
    Note: you can use the Meta attribute 'default_manager_name' to specify a different default manager.
    The 'get_queryset()' method of a manager returns the QuerySet that will be executed. We override
    this method to include your custom filter in the final QuerySet (i.e. we only want ones that are
    published).
    """
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    """
    This class is used to describe what a Post ought to contain.
    Upon writing the model we would have to 'python manage.py makemigrations' to create
    a migration file which will be added to this apps migrations folder. This file contains
    instructions on how to build the table that relates to this model for the database.
    To build teh database we use 'python manage.py migrate' which grabs all the migration
    files in the migrations directory across all apps and builds the tables.
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        We will use the 'get_absolute_url' method in our templates to link to specific posts
        """
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])
