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
	tasks = Task.objects.filter(user=request.user).order_by('-id')
	return render(request, 'home.html', {"form" : form, "tasks" : tasks})

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
	def post(self, request):
		data = request.data
		serializer = TaskSerializer(data=data)
		
		if not serializer.is_valid():
			return Response(serializer.errors)

		serializer.save(user=request.user)
		return Response({'data' : serializer.data})

	def put(self, request, tid):
		task = Task.objects.get(id=tid)

		if task.is_completed == False:
			data = {"is_completed" : True}
			task_is_completed = "True"
		else:
			data = {"is_completed" : False}
			task_is_completed = "False"

		serializer = TaskSerializer(instance=task, data=data, partial=True)

		if not serializer.is_valid():
			return Response(serializer.errors)

		serializer.save()

		return Response({"completed":task_is_completed})

	def delete(self, request, tid):
		if not Task.objects.filter(id=tid):
			return Response({"deleted":"False"})

		task = Task.objects.get(id=tid)
		task.delete()

		return Response({"deleted":"True"})

'''class AddTask(APIView):
	def post(self, request):
		data = request.data
		serializer = TaskSerializer(data=data)
		
		if not serializer.is_valid():
			return Response(serializer.errors)

		serializer.save(user=request.user)
		return Response({'data' : serializer.data})

class CompTask(APIView):
	def put(self, request, tid):
		task = Task.objects.get(id=tid)

		if task.is_completed == False:
			data = {"is_completed" : True}
			task_is_completed = "True"
		else:
			data = {"is_completed" : False}
			task_is_completed = "False"

		serializer = TaskSerializer(instance=task, data=data, partial=True)

		if not serializer.is_valid():
			return Response(serializer.errors)

		serializer.save()

		return Response({"completed":task_is_completed})

class DeleteTask(APIView):
	def delete(self, request, tid):
		if not Task.objects.filter(id=tid):
			return Response({"deleted":"False"})

		task = Task.objects.get(id=tid)
		task.delete()

		return Response({"deleted":"True"})'''