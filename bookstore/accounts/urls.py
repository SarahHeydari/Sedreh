from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('purchased-books/', PurchasedBooksView.as_view(), name='purchased-books'),
    path('nearest-bookshops/', NearestBookshopsView.as_view(), name='nearest-bookshops'),
    #path('return-book/<int:book_id>/', ReturnBookView.as_view(), name='return-book'),
]
