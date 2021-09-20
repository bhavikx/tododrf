from django.urls import path
from .views import homeView, loginView, signupView, logoutView, TaskAPI #AddTask, CompTask, DeleteTask

urlpatterns = [
	path('', homeView, name="home"),
	path('signup/', signupView, name="signup"),
	path('login/', loginView, name="login"),
	path('logout/', logoutView, name="logout"),

    path('add-task/', TaskAPI.as_view()),
    path('comp-task/<str:tid>', TaskAPI.as_view()),
    path('delete-task/<str:tid>', TaskAPI.as_view()),
]

''' 
	path('add-task/', AddTask.as_view()),
    path('comp-task/<str:tid>', CompTask.as_view()),
    path('delete-task/<str:tid>', DeleteTask.as_view()),
'''