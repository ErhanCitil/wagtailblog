from django.db import models

from wagtail.models import Page


# Create your models here.
class HomePage(Page):
    pass


class BlogPage(Page):
    pass


class BlogDetailPage(Page):
    pass


class ContactPage(Page):
    pass


class AboutPage(Page):
    pass
