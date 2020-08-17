from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,UploadForm
from django.contrib.auth.decorators import login_required
from .models import Profile,Projects,Events
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import EventsSerializer,ProfileSerializer,ProjectsSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form':form})


@login_required(login_url='login')
def index(request):
    """
    view function renders the landing page
    """
    current_user = request.user
    all_projects = Projects.objects.all()
    return render(request, 'index.html', {'all_projects':all_projects})


@login_required(login_url='login')
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save() 
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile,data=request.POST, files=request.FILES)
        my_projects = Projects.objects.filter(project_user=current_user)
        
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'my_projects':my_projects    
    }
    return render(request, 'profile.html', context)

def search_results(request):
    """
    view function returns the searched projects
    """
    if 'projects' in request.GET and request.GET["projects"]:
        project_search = request.GET.get("projects")
        searched_projects = Projects.get_projects(project_search)
        message = f"{project_search}"

        return render(request, 'search.html',{"message":message,"projects": searched_projects})

    else:
        message = "You haven't searched for any user"
        return render(request, 'search.html',{"message":message})

@login_required(login_url='login')
def project(request, project_id):
    try:
        project = Projects.objects.get(id=project_id)
    except Projects.DoesNotExist:
        raise Http404()
    return render(request, "project.html", {'project':project})

@login_required(login_url='login')
def upload_form(request):
    current_user = request.user.profile
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploaded_by = current_user
            image.save()
            messages.success(request, f'You have uploaded the project!')
            return redirect('index')
    else:
        form = UploadForm()
    return render(request, 'post.html', {'uploadform': form})

class EventList(APIView):
    def get(self, request, formart=None):
        all_events = Events.objects.all()
        serializers = EventsSerializer(all_events, many=True)
        return Response(serializers.data)

    def post(self, request, formart=None):
        serializers = EventsSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_event(self,pk):
        try:
            return Events.objects.get(pk=pk)
        except Events.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        event = self.get_event(pk)
        serializers = EventsSerializer(event)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        event = self.get_event(pk)
        serializers = EventsSerializer(event, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_event(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileList(APIView):
    def get(self, request, formart=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)

    def post(self, request, formart=None):
        serializers = ProfileSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_profile(self,pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        prof = self.get_profile(pk)
        serializers = ProfileSerializer(prof)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        prof = self.get_profile(pk)
        serializers = ProfileSerializer(prof, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        prof = self.get_profile(pk)
        prof.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectsList(APIView):
    def get(self, request, formart=None):
        all_projects = Projects.objects.all()
        serializers = ProjectsSerializer(all_projects, many=True)
        return Response(serializers.data)

    def post(self, request, formart=None):
        serializers = ProjectsSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectsDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_projects(self,pk):
        try:
            return Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        project = self.get_projects(pk)
        serializers = ProjectsSerializer(project)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        project = self.get_projects(pk)
        serializers = ProjectsSerializer(project, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_projects(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)