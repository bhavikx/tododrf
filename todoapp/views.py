from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .decorators import login_requires, unauthenticated
from .forms import SignupForm, TaskForm
from .models import Task, User
from .serializers import TaskSerializer

@login_requires
def homeView(request):
	form = TaskForm()
	tasks = Task.objects.filter().order_by('-id')
	context = {"form" : form, "tasks" : tasks}
	return render(request, 'home.html', context)

@unauthenticated
def signupView(request):
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			return render(request, 'login.html')

		else:
	 		messages.info(request, "Try Again")

	form = SignupForm()

	context = {'form' : form,}
	return render(request, 'signup.html', context)

@unauthenticated
def loginView(request):
	if request.method == 'POST':
	 	email = request.POST.get('email')
	 	password = request.POST.get('password')
	 	user = authenticate(request, email = email, password = password)

	 	if user:
	 		login(request, user)
	 		return redirect('home')

	 	else:
	 		messages.info(request, "Email or Password incorrect... try again.")

	return render(request, 'login.html')

def logoutView(request):
    logout(request)
    return redirect('login')

class TaskAPI(APIView):

	def get_object(self, id):
		try:
			return Task.objects.get(id=id)
		except Task.DoesNotExist:
			raise Http404

	def post(self, request):

		form = TaskForm(request.POST)
		if form.is_valid:
			task = form.save()

			task_id = task.id
			task = task.text

			context = {'task_id' : task_id, 'task' : task}

		return Response(context)

	def put(self, request, tid):
		task = self.get_object(tid)

		if task.is_completed == False:
			task.is_completed = True
		else:
			task.is_completed = False

		task.save()

		return Response(status=status.HTTP_204_NO_CONTENT)


	def delete(self, request, tid):
		print('tid')
		print(tid)

		task = self.get_object(tid)
		task.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)