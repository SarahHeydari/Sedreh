
from django.urls import path
from .views import BookListView, BuyBookView, ReturnBookView, CreateBookView, BuyBookByNameView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('buy/<int:pk>/', BuyBookView.as_view(), name='buy-book'),
    path('buy-by-name/', BuyBookByNameView.as_view(), name='buy-book-by-name'),  # 👈 مسیر جدید
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
    path('create/', CreateBookView.as_view(), name='create-book'),
]