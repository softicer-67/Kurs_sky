from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app.forms import CustomUserCreateForm, CustomAuthenticationForm, FileUploadForm
from app.models import *
from app.serializers import FileSerializer


def home(request):
    if request.user.is_authenticated:
        my_files = File.objects.filter(owner=request.user).order_by('owner')
        return render(request, 'app/home.html', {'my_files': my_files})
    else:
        return render(request, 'app/index.html')


class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def list(self, request, *args, **kwargs):

        ad_file = request.GET.get('file')
        if ad_file:
            self.queryset = self.queryset.filter(name__id__in=ad_file)
            print(self.queryset)
        serial = self.get_serializer(self.queryset, many=True)
        return Response(serial.data)


# def upload_file(request):
#     if request.method == 'POST':
#         form = LoadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/")
#     else:
#         form = LoadFileForm
#     return render(request, 'app/load_file.html', {'form': form})

class AddFileView(View):
    form_class = FileUploadForm
    template_name = 'app/add_file.html'
    success_url = reverse_lazy('home')
    success_message = 'File added successfully!'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = self.request.user
            file.save()

        return redirect(self.success_url)


class DetailFileView(LoginRequiredMixin, DetailView):
    template_name = 'app/detail_info.html'

    def get_object(self):
        try:
            return Logs.objects.get(file=self.kwargs['pk'])
        except Exception:
            return None


# class FileDelete(View):
#     def get(self, request, slug):
#         file = File.objects.get(name__exact=slug)
#         print(file)
#         return render(request, 'app/delete.html', context={'file': file})
#
#     def post(self, request, slug):
#         file = File.objects.get(name__exact=slug)
#         file.delete()
#         return redirect(reverse_lazy('home'))


class RegisterUser(CreateView):
    form_class = CustomUserCreateForm
    template_name = 'app/register.html'

    def get_success_url(self):
        return reverse_lazy('home')


class LoginUser(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'app/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class FileDelete(LoginRequiredMixin, DeleteView):
    model = File
    template_name = 'app/delete.html'
    success_url = reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


