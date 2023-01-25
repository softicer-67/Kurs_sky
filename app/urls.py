from django.urls import path, include
from rest_framework import routers

from app.views import *

# router = routers.DefaultRouter()
# router.register(r'file', FileViewSet)


urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('detail_file/<int:pk>/', DetailFileView.as_view(), name='detail_info'),
    path('add_file/', AddFileView.as_view(), name='load_file'),
    path('delete/<int:pk>/', FileDelete.as_view(), name='delete'),
    # path("", include(router.urls)),
]

