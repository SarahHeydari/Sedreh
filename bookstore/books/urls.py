from django.urls import path
from .views import BookListView, BuyBookView, ReturnBookView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('buy/<int:pk>/', BuyBookView.as_view(), name='buy-book'),
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
]
