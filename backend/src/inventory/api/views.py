from inventory.models import Bucket, Task
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import BucketSerializer, TaskSerializer


@api_view(["GET"])
def apiOverview(request):
    """
    This function will return all the api URLs.
    """

    api_urls = {
        "BucketList": "/bucket-list/",
        "BucketCreate": "/bucket-create/",
        "BucketUpdate": "/bucket-update/<str:pk>/",
        "BucketDelete": "/bucket-delete/<str:pk>/",
        "BucketTasksList": "/bucket/<str:bucket_pk>/tasks",
        "BucketTaskCreate": "bucket/<str:bucket_pk>/task-create/",
        "BucketTaskUpdate": "bucket/<str:bucket_pk>/task-update/<str:pk>/",
        "BucketTaskDelete": "bucket/<str:bucket_pk>/task-delete/<str:pk>/",
    }
    return Response(api_urls)


@api_view(["GET"])
def bucketList(request):
    """
    This function will return list of buckets
    """

    # get all items
    if request.method == "GET":
        buckets = Bucket.objects.all().order_by("-id")
        serializer = BucketSerializer(buckets, many=True)
        return Response(serializer.data)


@api_view(["POST"])
def bucketCreate(request):
    """
    This function will create an bucket
    """

    # insert a new record for an item
    if request.method == "POST":
        # data = {
        #     "name": request.data.get("name"),
        #     "description": request.data.get("description"),
        #     "price": float(request.data.get("price")),
        # }
        data = request.data

        serializer = BucketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "PUT"])
def bucketUpdate(request, pk):
    """
    This function will update an bucket
    """

    try:
        item = Bucket.objects.get(pk=pk)
    except Bucket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # update details of a single bucket
    if request.method == "PUT":
        serializer = BucketSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Another approach
    if request.method == "POST":
        serializer = BucketSerializer(instance=item, data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


@api_view(["DELETE"])
def bucketDelete(request, pk):
    """
    This function will delete an bucket
    """

    try:
        item = Bucket.objects.get(pk=pk)
    except Bucket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # return Response("Item successfully deleted!")


@api_view(["GET"])
def bucketTasks(request, bucket_pk):
    """
    This function will return item detail
    """

    try:
        item = Task.objects.filter(bucket__id=bucket_pk).order_by("-id")
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single item
    if request.method == "GET":
        serializer = TaskSerializer(item, many=True)
        return Response(serializer.data)


@api_view(["POST"])
def taskCreate(request, bucket_pk):
    """
    This function will create an item
    """

    # insert a new record for an item
    if request.method == "POST":
        # data = {
        #     "name": request.data.get("name")
        # }
        data = request.data
        serializer = TaskSerializer(data=data, bucket_pk=bucket_pk)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "PUT"])
def taskUpdate(request, bucket_pk, pk):
    """
    This function will update an item
    """

    try:
        task = Task.objects.get(pk=pk, bucket__id=bucket_pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # update details of a single task
    if request.method == "PUT":
        serializer = TaskSerializer(task, data=request.data, bucket_pk=bucket_pk)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Another approach
    if request.method == "POST":
        serializer = TaskSerializer(
            instance=task, data=request.data, bucket_pk=bucket_pk
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


@api_view(["DELETE"])
def taskDelete(request, bucket_pk, pk):
    """
    This function will delete an item
    """

    try:
        task = Task.objects.get(pk=pk, bucket__pk=bucket_pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # return Response("Item successfully deleted!")
