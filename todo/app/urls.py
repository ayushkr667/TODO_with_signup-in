from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('logIn/', views.login, name = 'logIn'),
    path('signup/', views.signup, name = 'signUp'),
    path('add-todo/', views.add_todo, name = 'add_todo'),
    path('delete-todo/<int:id>', views.delete_todo, name = 'delete_todo'),
    path('change-status/<int:id>/<str:status>', views.change_todo_status, name = 'change_status'),
    path('logout/', views.signout, name = 'logout'),
]
