from django.urls import path
from .views import Page, UpdateNews, NewsList, New_News, Old_News

urlpatterns = [
    path('', Page.as_view(), name='news-list'),
    path('<int:pk>/', UpdateNews.as_view(), name='news-detail'),
    path('<int:news_id>/filter/', NewsList.as_view(), name='news-list-filter'),
    path('new/', New_News.as_view(), name='new-news'),
    path('old/', Old_News.as_view(), name='old-news'),
]