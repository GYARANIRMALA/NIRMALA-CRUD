from rest_framework import serializers
from task1_app.models import Blog, Comments, User

class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = "__all__"

class CommentsSerializer(serializers.ModelSerializer):
    len_comment = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = "__all__"

    def get_len_comment(self,object):
        return len(object.comment)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = "__all__"
        exclude = [
            "password"
        ]