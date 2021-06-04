from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from .forms import TODOForm
from . models import TODO
from django.contrib.auth.decorators import login_required

# this decorator will never open home page till you logged in
# it will always redirect to login page
@login_required(login_url = 'logIn')

def home(request):
    if request.user.is_authenticated:
        user = request.user
        # this will get you all todos
        # todos = TODO.objects.all()
        form = TODOForm()
        #this will get you todo of logged in user only
        todos = TODO.objects.filter(user = user).order_by('priority')
        context = {
            'form' : form,
            'todos' : todos,
        }
        return render(request, 'todo/index.html', context = context)




def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            "form" : form
        }
        return render(request, 'todo/logIn.html', context = context)

    else:
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            context = {
                "form" : form
            }
            return render(request, 'todo/logIn.html', context = context)






def signup(request):
    # creating form
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form" : form
        }
        return render(request, 'todo/signUp.html', context = context)

    #creating user in post
    else:
        form = UserCreationForm(request.POST)
        context = {
            "form" : form
        }

        if form.is_valid():
            user = form.save()
            # if user is created
            if user is not None:
                return redirect('logIn')
        else:
            return render(request, 'todo/signUp.html', context = context)




def add_todo(request):
    # check if loggedin
    if request.user.is_authenticated:
        user = request.user

        form = TODOForm(request.POST)
        if form.is_valid():
            # make commit as false as user is not provided yet
            todo = form.save(commit = False)
            todo.user = user
            todo.save()
            return redirect("home")
        else:
            context = {
                "form" : form
            }
            return render(request, 'todo/index.html', context = context)
    else:
        return redirect('logIn')




def delete_todo(request, id ):
    TODO.objects.get(pk = id).delete()
    return redirect('home')


def change_todo_status(request, id, status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')




@login_required(login_url = 'logIn')
def signout(request):
    logout(request)
    return redirect('logIn')
