from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserProfileSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from books.models import Purchase, Bookshop, Book
from books.serializers import BookSerializer
from django.contrib.gis.db.models.functions import Distance


#--------------------------
from rest_framework import status

User = get_user_model()


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        profile_data = self.get_serializer(user).data

        # تسک ۲: لیست کتاب‌هایی که خریده
        purchased_books = Purchase.objects.filter(user=user).select_related('book')
        books = [p.book for p in purchased_books]
        books_data = BookSerializer(books, many=True).data

        # تسک ۳: نزدیک‌ترین کتاب‌فروشی‌ها
        nearest_shops_data = []
        if user.location:
            nearest_shops = Bookshop.objects.annotate(
                distance=Distance('location', user.location)
            ).order_by('distance')[:3]

            nearest_shops_data = [
                {
                    "name": shop.name,
                    "location": {
                        "latitude": shop.location.y,
                        "longitude": shop.location.x
                    },
                    "distance_m": round(shop.distance.m, 2)
                }
                for shop in nearest_shops
            ]

        return Response({
            "profile": profile_data,
            "purchased_books": books_data,
            "nearest_bookshops": nearest_shops_data
        })


class PurchasedBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        purchases = Purchase.objects.filter(user=user).select_related('book')
        books = [p.book for p in purchases]
        serialized_books = BookSerializer(books, many=True)
        return Response({"purchased_books": serialized_books.data})


class NearestBookshopsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.location:
            return Response({"error": "Location not set for user."}, status=400)

        nearest_shops = Bookshop.objects.annotate(
            distance=Distance('location', user.location)
        ).order_by('distance')[:3]

        data = [
            {
                "name": shop.name,
                "location": {
                    "latitude": shop.location.y,
                    "longitude": shop.location.x
                },
                "distance_m": round(shop.distance.m, 2)
            }
            for shop in nearest_shops
        ]
        return Response({"nearest_bookshops": data})


class CustomLoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer






# #-----------------------
# class ReturnBookView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         user = request.user
#         book_id = request.data.get("book_id")
#
#         if not book_id:
#             return Response({"error": "book_id is required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             book = Book.objects.get(id=book_id)
#         except Book.DoesNotExist:
#             return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
#
#         try:
#             purchase = Purchase.objects.get(user=user, book=book)
#             purchase.delete()
#             return Response({"message": f"You have successfully returned '{book.title}'."})
#         except Purchase.DoesNotExist:
#             return Response({"error": "You have not purchased this book."}, status=status.HTTP_400_BAD_REQUEST)
