"""
Serializers allows us to return any model object in a JSON response or object
"""

from rest_framework import serializers
from inventory.models import Bucket, Task


class BucketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucket
        fields = ("id", "name")


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "name", "done")

    def __init__(self, *args, **kwargs):
        self.bucket_pk = kwargs.pop("bucket_pk") if "bucket_pk" in kwargs else None
        super(TaskSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        task = Task(name=validated_data["name"])
        task.bucket = Bucket.objects.get(pk=self.bucket_pk)
        task.save()
        return task
