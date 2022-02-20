from django.urls import path
from . import views

urlpatterns = [
    path('get_cls/', views.get_classrooms,name='get_cls'),
    path('crud_cl/<slug:slug>/', views.crud_classroom, name='crud_cls'),
    path('gp_users/', views.gp_users, name='gp_users'),
    path('crud_user/<int:id>/', views.crud_user, name='crud_user'),
    path('cl_search/<str:subject>/<str:teacher>/', views.classroom_search, name='classroom_search'),

]
