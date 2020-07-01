from django.urls import path

from day04 import views

urlpatterns = [
    path("books/", views.BookAPIView.as_view()),
    path("books/<str:id>/", views.BookAPIView.as_view()),

    path("gen/", views.BookGenericAPIView.as_view()),
    path("gen/<str:id>/", views.BookGenericAPIView.as_view()),

    path("list/", views.BookListAPIVIew.as_view()),
    path("list/<str:id>/", views.BookListAPIVIew.as_view()),

    path("set/", views.BookGenericViewSet.as_view({"post": "user_login", "get": "user_register"})),
    path("set/<str:id>/", views.BookGenericViewSet.as_view({"post": "user_login"})),

]
