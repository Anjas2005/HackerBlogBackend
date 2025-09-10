from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import Best_News,Post_Best_News

post_router=DefaultRouter()
post_router.register(r'HackerAPI',Post_Best_News)

urlpatterns=[
    path('RecieveNews/',Best_News.as_view()),

]