from rest_framework import viewsets, status
from rest_framework.response import Response
from task1_app.models import Blog, Comments, User
from task1_app.serializers import BlogSerializer, CommentsSerializer, UserSerializer
import requests
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, JsonResponse
import uuid

from django.contrib.auth import authenticate

from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model
from cryptography.fernet import Fernet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework .exceptions import AuthenticationFailed
from rest_framework.views import APIView



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
    def create(self, request, *args, **kwargs):
        try:
            comment = Comments( 
                comment = request.data["comment"],
                blog_id = Blog.objects.get(id=request.data["blog_id"]),
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
            comments = Comments.objects.filter().order_by('likes')
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
                if request.data["likes"] < 0:
                    return Response({"error": "likes should not accept negative values"}, status=status.HTTP_400_BAD_REQUEST)
                comment.likes = request.data["likes"]
            if "dislike" in request.data:
                if request.data["dislike"] < 0:
                    return Response({"error": "dislike values should not accept negative values"}, status=status.HTTP_400_BAD_REQUEST)
                comment.dislike = request.data["dislike"]
            if "status" in request.data:
                return Response({"error": "status should not be updated"}, status=status.HTTP_400_BAD_REQUEST)
            if "active" in request.data:
                return Response({"error": "active should not be updated"}, status=status.HTTP_400_BAD_REQUEST)
            if "order" in request.data:
                if request.data["order"] < 0 :
                    return Response({"error": "Order should not be negitive"}, status=status.HTTP_400_BAD_REQUEST)
                comment.order = request.data["order"]
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
def show_comment(request,id):
    try:
        if request.method == 'POST':
            data = JSONParser().parse(request)
            try:
                blog_id = Blog.objects.get(id=id)
            except Exception:
                return JsonResponse({"error": "Invalid blog id"}, status=status.HTTP_400_BAD_REQUEST)
            comment = Comments(
                comment = data["comment"],
                blog_id = blog_id,
            )
            comment.save()
            return JsonResponse(CommentsSerializer(comment).data,status=status.HTTP_201_CREATED)
    except Exception as err:
        print("error show_comment create",err)
        return Response({"error":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def encryptPassword(password):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encpassword = fernet.encrypt(password.encode())
    return encpassword

def decryptPassword(password):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encpassword = fernet.decrypt(password.decode())
    return encpassword

class UserApi(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        try:
            try:
                User.objects.get(username=request.data["username"])
                return Response({"error": "Given username is already exist"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                pass
            try:
                User.objects.get(email=request.data["email"])
                return Response({"error": "Given email is already exist"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                pass
            try:
                if request.data["role"] not in [User.RoleTypes.admin,User.RoleTypes.support,User.RoleTypes.user]:
                    return Response({"error":"Invalid role"},status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                pass
            try:
                if request.data["status"] not in [User.StatusTypes.inactive,User.StatusTypes.active,User.StatusTypes.blocked]:
                    return Response({"error":"Invalid status"},status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                pass

            # encrypted_password = encryptPassword(request.data["password"])
            # print("encrypted_password --->",encrypted_password)

            # decrypted_password = encryptPassword(request.data["password"])
            # print("decrypted_password --->",decrypted_password)

            user = User(
                username = request.data["username"],
                email = request.data["email"],
                password = request.data["password"],
                # password = encrypted_password,
                fullname = request.data["fullname"],
                role = request.data["role"],
                status = request.data["status"],
                active = request.data["active"],
                created_by = request.data["created_by"],
                updated_by = request.data["updated_by"],
            )
            user.save()
            return Response(
                UserSerializer(user).data, status=status.HTTP_201_CREATED
            )
        except Exception as err:
            print("error UserApi create")
            return Response({"error":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            users = User.objects.filter()
            return Response(
                UserSerializer(users, many=True).data, status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error UserApi get")
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs["pk"])
            return Response(
                UserSerializer(user).data, status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error UserApi retrieve")
            return Response({"error":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs["pk"])

            if "username" in request.data:
                user.username = request.data["username"]
            if "email" in request.data:
                user.email = request.data["email"]
            if "password" in request.data:
                user.password = request.data["password"]
            if "fullname" in request.data:
                user.fullname = request.data["fullname"]
            if "role" in request.data:
                try:
                    if request.data["role"] not in [User.RoleTypes.admin,User.RoleTypes.support,User.RoleTypes.user]:
                        return Response({"error":"Invalid role"},status=status.HTTP_400_BAD_REQUEST)
                except Exception:
                    pass 
            if "status" in request.data:
                try:
                    if request.data["status"] not in [User.StatusTypes.inactive,User.StatusTypes.active,User.StatusTypes.blocked]:
                        return Response({"error":"Invalid status"},status=status.HTTP_400_BAD_REQUEST)
                except Exception:
                    pass
            if "active" in request.data:
                return Response({"error": "active should not be updated"}, status=status.HTTP_400_BAD_REQUEST)
            if "created_by" in request.data:
                user.created_by = request.data["created_by"]
            if "updated_by" in request.data:
                user.updated_by = request.data["updated_by"]
            user.save()
            return Response(
                UserSerializer(user).data, status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error UserApi update")
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs["pk"])
            user.delete()
            return Response(
                status=status.HTTP_200_OK
            )
        except Exception as err:
            print("error UserApi delete")
            return Response({"error": "This user was Deleted"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginApi(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            user = authenticate(
                email=request.data["email"], password=request.data["password"]
            )
            if not user:
                return Response(
                    {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
                )
            serializer = UserSerializer(user).data
            response = requests.post(url="http://127.0.0.1:8000/user/api/token/", data={
                "email" : request.data["email"],
                "password" :request.data["password"],
            })
            token = response.json()
            serializer["refresh"] = token["refresh"]
            serializer["access"] = token["access"]
            return Response(serializer, status=status.HTTP_200_OK)
        except Exception as err:
            print("error --->",err)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

