from rest_framework import viewsets, status
from rest_framework.response import Response
from task1_app.models import Blog
from task1_app.serializers import BlogSerializer
import requests
from datetime import datetime

class BlogApi(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            # if request.data["status"] not in [Blog.StatusTypes.draft,Blog.StatusTypes.published,Blog.StatusTypes.pending]:
            #     return Response({"error":"Invalid status"},status=status.HTTP_400_BAD_REQUEST)

            # blog = Blog(
            #     title = request.data["title"],
            #     description = request.data["description"],
            #     primary_image = request.data["primary_image"],
            #     likes = request.data["likes"],
            #     views = request.data["views"],
            #     status = request.data["status"],
            #     active = request.data["active"],
            #     order = request.data["order"],
            #     created_by = request.data["created_by"],
            #     updated_by = request.data["updated_by"],
            # )
            # blog.save()
            # return Response(
            #     BlogSerializer(blog).data, status=status.HTTP_201_CREATED
            # )

            serializer = BlogSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print("error BlogApis create",err)
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            blogs = Blog.objects.filter().order_by('views')
            return Response(
                BlogSerializer(blogs, many=True).data, status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error BlogApis get")
            return Response({"error":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            blog = Blog.objects.get(id=kwargs["pk"])
            return Response(
                BlogSerializer(blog).data, status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error BlogApis retrieve")
            return Response({"error":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args,**kwargs):
        try:
            blog = Blog.objects.get(id=kwargs["pk"])

            if "title" in request.data:
                blog.title = request.data["title"]
            if "description" in request.data:
                blog.description = request.data["description"]
            if "primary_image" in request.data:
                blog.primary_image = request.data["primary_image"]
            if "likes" in request.data:
                blog.likes = request.data["likes"]
            if "views" in request.data:
                blog.views = request.data["views"]
            if "created_by" in request.data:
                blog.created_by = request.data["created_by"]
            if "updated_by" in request.data:
                blog.updated_by = request.data["updated_by"]
            if "status" in request.data:
                try:
                    existing_blog = Blog.objects.get(status=request.data["status"])
                    if blog.id != existing_blog.id:
                        return Response({"error": "status should not be updated"}, status=status.HTTP_400_BAD_REQUEST)
                except Exception:
                    pass
                blog.status = request.data["status"]

                # return Response({"error": "Status should not be updated"}, status=status.HTTP_400_BAD_REQUEST)
            if "active" in request.data:
                return Response({"error": "active should not be updated"}, status=status.HTTP_400_BAD_REQUEST)
            if "order" in request.data:
                # n = request.data["order"]
                # if n < 0 :
                if request.data["order"] < 0 :
                    return Response({"error": "Order should not be negitive"}, status=status.HTTP_400_BAD_REQUEST)
                blog.order = request.data["order"]
            blog.save()
            return Response(
                BlogSerializer(blog).data, status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error BlogApis update")
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            blog = Blog.objects.get(active=True,id=kwargs["pk"])
            blog.active = False
            blog.save()
            return Response(
                {"error" : "This Book was Deleted"},
                status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error BlogApi destroy",err)
            return Response({"error" : str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



