from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from family.models import Family, Parent, Child
from family.api.serializers import FamilySerializer, ParentSerializer, ChildSerializer


class FamilyListCreateAPIView(APIView):

    def get(self, request):
        articles = Family.objects.all()
        serializer = FamilySerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = FamilySerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildListCreateAPIView(APIView):

    def get(self, request):
        articles = Child.objects.all()
        serializer = ChildSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)


class ChildDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Child, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ChildSerializer(article)
        return Response(serializer.data)


class ParentListCreateAPIView(APIView):

    def get(self, request):
        articles = Parent.objects.all()
        serializer = ParentSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)


class ParentDetailAPIView(APIView):
    def get_object(self, pk):
        article = get_object_or_404(Parent, pk=pk)
        return article

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ParentSerializer(article, context={'request': request})
        return Response(serializer.data)

# class ArticleDetailAPIView(APIView):
#
#     def get_object(self, pk):
#         article = get_object_or_404(Article, pk=pk)
#         return article
#
#     def get(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         article = self.get_object(pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
