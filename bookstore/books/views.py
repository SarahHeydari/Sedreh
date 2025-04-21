from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .models import Book, Purchase, County
from .serializers import BookSerializer
from accounts.models import CustomUser



class BookListView(generics.ListAPIView):
    queryset = Book.objects.filter(available=True)
    serializer_class = BookSerializer



class CreateBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.user_type != 'seller':
            return Response({"error": "Only sellers can add books."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            return Response({"message": "Book created successfully", "book_id": book.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BuyBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        tehran = County.objects.first()
        user_location = request.user.location

        if not tehran or not user_location or not tehran.geometry.contains(user_location):
            return Response({'error': 'You must be located inside Tehran to purchase.'}, status=403)

        if book.available and request.user.balance >= book.price:
            Purchase.objects.create(user=request.user, book=book)
            book.available = False
            book.save()
            request.user.balance -= book.price
            request.user.save()
            return Response({'message': 'Book purchased successfully'})

        return Response({'error': 'Insufficient balance or book unavailable'}, status=400)



class BuyBookByNameView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        book_name = request.data.get('title')
        if not book_name:
            return Response({'error': 'Book name is required'}, status=status.HTTP_400_BAD_REQUEST)

        book = Book.objects.filter(Q(title__icontains=book_name), available=True).first()
        if not book:
            return Response({'error': 'Book not found or unavailable'}, status=status.HTTP_404_NOT_FOUND)

        tehran = County.objects.first()
        user_location = request.user.location

        if not tehran or not user_location or not tehran.geometry.contains(user_location):
            return Response({'error': 'You must be located inside Tehran to purchase.'}, status=status.HTTP_403_FORBIDDEN)

        if request.user.balance < book.price:
            return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

        Purchase.objects.create(user=request.user, book=book)
        book.available = False
        book.save()
        request.user.balance -= book.price
        request.user.save()

        return Response({'message': f'Book \"{book.title}\" purchased successfully'})


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
