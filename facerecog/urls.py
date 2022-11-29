from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.http import StreamingHttpResponse,request, HttpResponse
from facerecog.feed import Video, gen, responser



urlpatterns = [ 
    path('create_user', views.register),
    # path('responser/feed/', lambda r, slug: StreamingHttpResponse(streaming_content=(responser(request, 0, slug)), content_type='multipart/x-mixed-replace; boundary=frame')),
    # path('responser/detect/<slug:slug>/', lambda r, slug: StreamingHttpResponse(responser(request, 1, slug), content_type='text/html')),
    path('retrain', views.rtrain),
    # path('feed/<slug:slug>/', views.feed),
    re_path(r'^detect/(?P<slug>[0-9]+(?:\.[0-9]+){3})/$', views.detect),
    re_path(r'^feed/(?P<slug>[0-9]+(?:\.[0-9]+){3})/$', views.feed)
]   