from django.urls import path
from .views import *
from .views_files import *


app_name="base"

urlpatterns = [
    path('classrooms_pdf/',classrooms_pdf,name='classrooms-pdf' ),
    path('classrooms_csv/',classrooms_csv,name='classrooms-csv' ),
    path('classrooms_txt/',classrooms_txt,name='classrooms_text' ),
    path('register/',RegisterPage,name='register' ),
    path('login/', LoginPage, name='login'),
    path('logout/', LogoutUser, name='logout'),
    path('home/', HomePage, name='home'),
    path('create_classroom/', CreateClassroom, name='create-classroom'),
    path('update_profile/', UpdateUser, name='update-profile'),
    path('update_classroom/<slug:slug>/', UpdateClassroom, name='update-classroom'),
    path('classroom/<slug:slug>',PageClassroom, name='classroom'),
    path('profile/<int:id>/', UserProfile, name='user'),
    path('delete_profile/', DeleteUser, name='delete-profile'),
    path('delete_classroom/<slug:slug>', DeleteClassroom, name='delete-classroom'),
    path('delete_message/<int:id>', DeleteMessage, name='delete-message'),

]
