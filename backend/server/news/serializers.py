from rest_framework import serializers
from django.contrib.auth.models import User

from . models import Post, Image, Document, Comment

class RecursiveSerializer(serializers.Serializer):
  
  def to_representation(self, value):
    serializer = self.parent.parent.__class__(value, context=self.context)
    return serializer.data

class FilterCommentListSerializer(serializers.ListSerializer):

  def to_representation(self, data):
    data = data.filter(parent=None)
    return super().to_representation(data)


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username']

# class NoteSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Note
#     fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Image
    fields = '__all__'

class DocSerializer(serializers.ModelSerializer):
  class Meta:
    model = Document
    fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    #note = serializers.SerializerMethodField()
    #docs = DocSerializer(many=True)
    
    def get_images(self, obj):
        queryset = Image.objects.filter(post_id=obj.id)
        serializer = ImageSerializer(queryset, many=True)
        return serializer.data

    # def get_note(self, obj):
    #     queryset = Note.objects.filter(post_id=obj.id)
    #     serializer = NoteSerializer(queryset, many=True)
    #     return serializer.data

    class Meta:
        model = Post
        fields = '__all__'

class PostViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'views']

class CommentSerializer(serializers.ModelSerializer):
  children = RecursiveSerializer(many=True, default='', read_only=True)

  class Meta:
    list_serializer_class = FilterCommentListSerializer
    model = Comment
    fields = '__all__'

class SimpleCommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'