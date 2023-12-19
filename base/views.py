from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required



def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:#if the user is already logged, then they cannot access the login link
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'user does not exist')


        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Provide a more detailed error message
            messages.error(request, "Invalid username or password. Please try again.")
            # Or you can directly add the error message to the context
            # context = {'error_message': "Invalid username or password. Please try again."}
            # return render(request, 'base/login_register.html', context)
    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)#Do not save the form in the database immediately so as to clean the details of the new user
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Error occured during registration')
    context = {'page': page, 'form':form}
    return render(request, 'base/login_register.html', context)

def home(request):
    # return HttpResponse('Home page')#return http response to home page
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q ) | 
                                Q(name__icontains = q) | 
                                Q(description__icontains = q))#query our database(room list) and filter our rooms based on name description and topic
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
    context = {'rooms':rooms, 'topics': topics, 'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    user_rooms = user.room_set.all()
    user_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':user_rooms,'room_messages':user_messages,'topics':topics}
    return render(request, 'base/profile.html',context)

def room(request, pk):
    # return HttpResponse('Room')
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all().order_by('-created')#Gvies the set of messages for the specific room object and order them based on newest created first
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))
        room.participants.add(request.user)#if a user engages in the chat then add them to the participants list
        return redirect('room', pk=room.id)
    context = {'room':room, 'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')#obtain the topic from the form, present in the room_form.html
        topic, created = Topic.objects.get_or_create(name=topic_name)
        #Manually create the room
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),#obtain the room name from the name field in the form present in the room_form.html
            description = request.POST.get('description')
        )
        return redirect('home')#redirect back to home page
    context = {'form' : form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You are not allowed to update the room!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')#obtain the topic from the form, present in the room_form.html
        topic, created = Topic.objects.get_or_create(name=topic_name)
        #obtain the new updated details of the room
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics,'room':room}
    return render(request, 'base/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    delete = 'room'
    room = Room.objects.get(id = pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed to delete the room!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':room,'delete':delete})

@login_required(login_url='login')
def deleteMsg(request, pk):
    delete = 'msg'
    msg = Message.objects.get(id = pk)

    if request.user != msg.user:
        return HttpResponse('You are not allowed to delete the message!!')
    
    if request.method == 'POST':
        msg.delete()
        return redirect('room',pk=msg.room.id)
    return render(request,'base/delete.html',{'obj':msg,'delete':delete})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('profile', pk = user.id)
        
    context = {'form':form}
    return render(request,'base/update-user.html',context)


def topicsPage(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''
    topics = Topic.objects.filter(name__icontains = q)
    context = {'topics':topics}
    return render(request, 'base/topics.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request,'base/activity.html', context)