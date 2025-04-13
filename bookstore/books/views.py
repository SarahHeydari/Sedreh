from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Purchase
from .serializers import BookSerializer
from django.shortcuts import get_object_or_404

# list of user's book
class BookListView(generics.ListAPIView):
    queryset = Book.objects.filter(available=True)
    serializer_class = BookSerializer

# api for return three closedt bookstore to location of user

class BuyBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if book.available and request.user.balance >= book.price:
            Purchase.objects.create(user=request.user, book=book)
            book.available = False
            book.save()
            request.user.balance -= book.price
            request.user.save()
            return Response({'message': 'Book purchased successfully'})
        return Response({'error': 'Insufficient balance or book unavailable'}, status=400)


class ReturnBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        purchase = get_object_or_404(Purchase, user=request.user, book_id=pk)
        purchase.book.available = True
        purchase.book.save()
        request.user.balance += purchase.book.price
        request.user.save()
        purchase.delete()
        return Response({'message': 'Book returned successfully'})
