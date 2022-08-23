from rest_framework import viewsets, status
from rest_framework.response import Response
from task1_app.models import Blog, Comments
from task1_app.serializers import BlogSerializer, CommentsSerializer
import requests
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt,csrf_protect #Add this
from django.http import HttpResponse, JsonResponse
import uuid


class BlogApi(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            if request.data["status"] not in [Blog.StatusTypes.Draft,Blog.StatusTypes.Published,Blog.StatusTypes.Pending]:
                return Response({"error":"Invalid status"},status=status.HTTP_400_BAD_REQUEST)

            if request.data["order"] < 0 :
                return Response({"error": "Order should not be negitive"}, status=status.HTTP_400_BAD_REQUEST)
   
            blog = Blog(
                title = request.data["title"],
                description = request.data["description"],
                primary_image = request.data["primary_image"],
                likes = request.data["likes"],
                views = request.data["views"],
                status = request.data["status"],
                active = request.data["active"],
                order = request.data["order"],
                created_by = request.data["created_by"],
                updated_by = request.data["updated_by"],
            )
            blog.save()
            return Response(
                BlogSerializer(blog).data, status=status.HTTP_201_CREATED
            )
            print("Hello")
            # serializer = BlogSerializer(data=request.data)
            # if serializer.is_valid():
            #     serializer.save()
            #     return Response(
            #         serializer.data, status=status.HTTP_201_CREATED
            #     )
            # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print("error BlogApis create",err)
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            blogs = Blog.objects.filter(active=True).order_by('order')
            blogs_serializer = BlogSerializer(blogs, many=True).data
            try:
                for data in blogs_serializer:
                    try:
                        comments_list = Comments.objects.filter(blog_id=data["id"])
                        comments_serailizer = CommentsSerializer(comments_list,many=True).data
                        data["comments"] = comments_serailizer
                    except Exception as err:
                        print("error1 --->",err)
                        pass
            except Exception as err:                        
                print("error2 --->",err)
                pass
            return Response(
                blogs_serializer, status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error BlogApis get")
            return Response({"error":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            blog = Blog.objects.get(id=kwargs["pk"])
            blogs_serializer = BlogSerializer(blog).data
            blogs_serializer["comments"] = []
            try:
                comments_list = Comments.objects.filter(blog_id=blogs_serializer["id"])
                blogs_serializer["comments"] = CommentsSerializer(comments_list,many=True).data
            except Exception:
                pass
            return Response(
                blogs_serializer, status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error BlogApis retrieve")
            return Response({"error":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args,**kwargs):
        try:
            blog = Blog.objects.get(id=kwargs['pk'])

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
                    if request.data["status"] not in [Blog.StatusTypes.Draft,Blog.StatusTypes.Published,Blog.StatusTypes.Pending]:
                        return Response({"error":"Invalid status"},status=status.HTTP_400_BAD_REQUEST)
                except Exception:
                    pass
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
            blog = Blog.objects.get(id=kwargs['pk'])
            blog.delete()
            return Response(
                {"error" : "This Book was Deleted"}, status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error BlogApi destroy",err)
            return Response({"error" : str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CommentsApi(viewsets.ViewSet):

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        try:
            comment = Comments(
                comment = request.data["comment"],
                blog_id = Blog.objects.get(id=kwargs['pk']),
                likes = request.data["likes"],
                dislike = request.data["dislike"],
                status = request.data["status"],
                active = request.data["active"],
                order = request.data["order"],
                created_by = request.data["created_by"],
                updated_by = request.data["updated_by"],
            )
            comment.save()
            return Response(
                CommentsSerializer(comment).data, status=status.HTTP_201_CREATED
            )
        except Exception as err:
            print("error CommentsApi create",err)
            return Response({"error":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            comments = Comments.objects.filter().order_by('comment')
            return Response(
                CommentsSerializer(comments, many=True).data, status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error Commentspi get")
            return Response({"error":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            comment = Comments.objects.get(id=kwargs['pk'])
            return Response(
                CommentsSerializer(comment).data, status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error CommentsApi read")
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            comment = Comments.objects.get(id=kwargs['pk'])

            if "comment" in request.data:
                comment.comment = request.data["comment"]
            if "blog_id" in request.data:
                comment.blog_id = Blog.objects.get(blog_id=request.data["blog_id"])
            if "likes" in request.data:
                comment.likes = request.data["likes"]
            if "dislike" in request.data:
                comment.dislike = request.data["dislike"]
            if "status" in request.data:
                comment.status = request.data["status"]
            if "active" in request.data:
                comment.active = request.data["active"]
            if "created_by" in request.data:
                comment.created_by = request.data["created_by"]
            if "updated_by" in request.data:
                comment.updated_by = request.data["updated_by"]
            comment.save()
            return Response(
                CommentsSerializer(comment).data, status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error CommentApi update")
            return Response({"error":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            comment = Comments.objects.get(id=kwargs['pk'])
            comment.delete()
            return Response(
                status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error CommentsApi destroy",err)
            return Response({"error": "This Object was Deleted"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def show_comment(request,id,comment):
    try:
        try:
            blog_id = Blog.objects.get(id=id)
        except Exception:
            return JsonResponse({"error": "Invalid blog id"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comments(
            comment = comment,
            blog_id = blog_id,
        )
        comment.save()
        return JsonResponse(CommentsSerializer(comment).data,status=status.HTTP_201_CREATED)
    except Exception as err:
        print("error show_comment create",err)
        return Response({"error":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
             