import json

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from inventory.api.serializers import BucketSerializer, TaskSerializer
from inventory.models import Bucket, Task

# Creating an client object
client = Client()


class GetAllItemsTest(TestCase):
    """ Test module for GET all Buckets / Bucket Tasks API """

    def setUp(self):
        bucket1 = Bucket.objects.create(name="Bucket 1")
        self.bucket1 = bucket1
        Bucket.objects.create(name="Bucket 2")

        Task.objects.create(name="Task 1", bucket=bucket1)

    def test_get_all_items(self):
        # get API response
        response = client.get(reverse("bucket-list"))
        task_response = client.get(
            reverse("bucket-tasks", kwargs={"bucket_pk": self.bucket1.pk})
        )
        # get data from db
        buckets = Bucket.objects.all()
        bucket_tasks = Task.objects.filter(bucket=self.bucket1)

        serializer = BucketSerializer(buckets, many=True)
        task_serializer = TaskSerializer(bucket_tasks, many=True)

        # Checking for Bucket
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checking for Bucket Tasks
        self.assertEqual(task_response.data, task_serializer.data)
        self.assertEqual(task_response.status_code, status.HTTP_200_OK)


class CreateNewItemTest(TestCase):
    """ Test module for inserting a new Bucket / Bucket Task """

    def setUp(self):
        # Bucket Payload Data
        self.valid_payload_for_bucket = {"name": "Bucket 1"}
        self.invalid_payload_for_bucket = {"name": ""}

        # Task Payload Data
        self.valid_payload_for_task = {"name": "Task 1"}
        self.invalid_payload_for_task = {"name": ""}

    def test_create_valid_item(self):
        # Checking for Bucket
        response = client.post(
            reverse("bucket-create"),
            data=json.dumps(self.valid_payload_for_bucket),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Checking for Task
        bucket_id = Bucket.objects.create(name="Bucket").id
        task_response = client.post(
            reverse(
                "task-create",
                kwargs={"bucket_pk": bucket_id},
            ),
            data=json.dumps(self.valid_payload_for_task),
            content_type="application/json",
        )
        self.assertEqual(task_response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_item(self):
        # Checking for Bucket
        response = client.post(
            reverse("bucket-create"),
            data=json.dumps(self.invalid_payload_for_bucket),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Checking for Task
        bucket_id = Bucket.objects.create(name="Bucket").id
        task_response = client.post(
            reverse(
                "task-create",
                kwargs={"bucket_pk": bucket_id},
            ),
            data=json.dumps(self.invalid_payload_for_task),
            content_type="application/json",
        )
        self.assertEqual(task_response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleItemTest(TestCase):
    """ Test module for updating an existing Bucket / Bucket Task record """

    def setUp(self):
        self.bucket = Bucket.objects.create(name="Bucket")
        self.task = Task.objects.create(name="Task", bucket=self.bucket)

        # Payload data for Bucket
        self.valid_payload_for_bucket = {"name": "New Bucket"}
        self.invalid_payload_for_bucket = {"name": ""}

        # Payload data for Task
        self.valid_payload_for_task = {"name": "New Task"}
        self.invalid_payload_for_task = {"name": ""}

    def test_valid_update_item(self):
        # Checking for Bucket
        response = client.put(
            reverse("bucket-update", kwargs={"pk": self.bucket.pk}),
            data=json.dumps(self.valid_payload_for_bucket),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Checking for Task
        response = client.put(
            reverse(
                "task-update", kwargs={"bucket_pk": self.bucket.pk, "pk": self.task.pk}
            ),
            data=json.dumps(self.valid_payload_for_task),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_item(self):
        # Cheking for Bucket
        response = client.put(
            reverse("bucket-update", kwargs={"pk": self.bucket.pk}),
            data=json.dumps(self.invalid_payload_for_bucket),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Checking for Task
        response = client.put(
            reverse(
                "task-update", kwargs={"bucket_pk": self.bucket.pk, "pk": self.task.pk}
            ),
            data=json.dumps(self.invalid_payload_for_task),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleItemTest(TestCase):
    """ Test module for deleting an existing Bucket / Bucket Task record """

    def setUp(self):
        self.bucket1 = Bucket.objects.create(name="Bucket1")
        self.task1 = Task.objects.create(name="Task1", bucket=self.bucket1)
        self.bucket2 = Bucket.objects.create(name="Bucket2")
        self.task2 = Task.objects.create(name="Task2", bucket=self.bucket2)

    def test_valid_delete_item(self):
        # Checking for Bucket
        response = client.delete(
            reverse("bucket-delete", kwargs={"pk": self.bucket1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Checking for Task
        task_response = client.delete(
            reverse(
                "task-delete",
                kwargs={"bucket_pk": self.bucket2.pk, "pk": self.task2.pk},
            )
        )
        self.assertEqual(task_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_item(self):
        # Checking for Bucket
        response = client.delete(reverse("bucket-delete", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Checking for Task
        task_response = client.delete(
            reverse("task-delete", kwargs={"bucket_pk": self.bucket1.pk, "pk": 30})
        )
        self.assertEqual(task_response.status_code, status.HTTP_404_NOT_FOUND)
