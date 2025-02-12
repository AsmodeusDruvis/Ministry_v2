from rest_framework import generics
from .models import News
from .serializers import NewsSerializer

class Page(generics.ListCreateAPIView):
    queryset = News.objects.order_by("date")
    serializer_class = NewsSerializer

class UpdateNews(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'pk'

class NewsList(generics.ListCreateAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        news_id = self.kwargs.get('news_id')
        if news_id:
            return News.objects.filter(pk__gt=news_id)

class New_News(generics.ListAPIView):
    queryset = News.objects.all().order_by('-date')[:10] 
    serializer_class = NewsSerializer

class Old_News(generics.ListAPIView):
    queryset = News.objects.all().order_by('date')[:10]
    serializer_class = NewsSerializer