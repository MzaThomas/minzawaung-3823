from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy
from hr_recruitments import models
from hr_recruitments import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.db.models import Q
from .models import ResumeModel
from django.contrib import messages

class SearchBy(View):

    def get(self, request):
        search = request.GET.get('search')
        if search:    
            resumes = ResumeModel.objects.filter(
                Q(name__icontains=search) | 
                Q(sequence__icontains=search) |
                Q(appointment_date__icontains=search) |
                Q(note__icontains=search) |
                Q(status__icontains=search) |
                Q(create_date__icontains=search)
            )
        else:      
            resumes = ResumeModel.objects.all()
        return render(request, 'resume_list.html', {'all_resumes': resumes})

class OrderBy(View):
    pass

class ResumeListView(LoginRequiredMixin, ListView):
	paginate_by = 3
	login_url = 'login'
	model = models.ResumeModel
	context_object_name = 'all_resumes'
	template_name = 'resume_list.html'

	def get_queryset(self):
		qs = super().get_queryset()
		order = self.request.GET.get("order")
		if order is not None:
			qs = ResumeModel.objects.all().order_by("-" + order)
		return qs

class ResumeCreateView(PermissionRequiredMixin, CreateView):
	permission_required = 'hr_recruitments.add_resumemodel'
	login_url = 'login'
	success_url = reverse_lazy("resume_list")
	model = models.ResumeModel
	form_class = forms.ResumeForm
	template_name = 'resume_create.html'

	def form_valid(self, form):
		response = super().form_valid(form)
		messages.success(self.request, 'Form saved successfully')
		return response

class ResumeUpdateView(PermissionRequiredMixin, UpdateView):
	permission_required = 'hr_recruitments.change_resumemodel'
	login_url = 'login'
	success_url = reverse_lazy("resume_list")
	model = models.ResumeModel
	form_class = forms.ResumeForm
	context_object_name = "resume"
	template_name = 'resume_update.html'

	def form_valid(self, form):
		response = super().form_valid(form)
		messages.success(self.request, 'Form updated successfully')
		return response

class ResumeDetailView(PermissionRequiredMixin, DetailView):
	permission_required = 'hr_recruitments.view_resumemodel'
	login_url = 'login'
	model = models.ResumeModel
	context_object_name = "resume"
	template_name = 'resume_detail.html'

class ResumeDeleteView(PermissionRequiredMixin, DeleteView):
	permission_required = 'hr_recruitments.delete_resumemodel'
	login_url = 'login'

	def get(self, request, pk):
		resume = models.ResumeModel.objects.get(id=pk)
		resume.delete()
		messages.success(request, 'Form deleted successfully.')
		return redirect('resume_list')