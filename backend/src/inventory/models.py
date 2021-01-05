from django.contrib.auth.models import User
from django.db import models


class Base(models.Model):
    """
    Base model inherited by other models
    """

    name = models.CharField(max_length=200, null=False)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="created_on")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="modified_on")

    class Meta:
        abstract = True
        ordering = ["-date_modified"]


class Bucket(Base):
    """
    Model for Bucket
    """

    user = models.ForeignKey(
        User,
        related_name="bucket",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta(Base.Meta):
        db_table = "bucket"

    def __str__(self):
        return self.name


class Task(Base):
    """
    Model for Task
    """

    bucket = models.ForeignKey(Bucket, related_name="items", on_delete=models.CASCADE)
    done = models.BooleanField(default=False)

    class Meta(Base.Meta):
        db_table = "task"
        ordering = ["done", "-date_modified"]

    def __str__(self):
        return self.name