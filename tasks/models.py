from django.db import models
from model_utils.models import TimeFramedModel
from taggit.managers import TaggableManager

# Create your models here.


class Task(TimeFramedModel):
    text = models.CharField(max_length=40)
    tag = TaggableManager()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text