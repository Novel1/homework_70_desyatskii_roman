from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView, DetailView

from webapp.forms import TrackerForm, ProjectForm
from webapp.models import Tracker, Project

from webapp.forms import SearchForm


# Create your views here.

class IndexView(ListView):
    template_name = 'tracker/index.html'
    model = Tracker
    context_object_name = 'tracker'
    ordering = ('created_at',)
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True)
        if self.search_value:
            query = Q(summary__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            if not context['paginator'].count:
                context['error'] = "Задачи не найдены"
        return context


class TrackerDetail(TemplateView):
    template_name = 'tracker/tracker_view.html'
    permission_required = 'webapp.change_tracker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracker'] = get_object_or_404(Tracker, pk=kwargs['pk'])
        return context


class TrackerAdd(LoginRequiredMixin, CreateView):
    template_name = 'tracker/tracker_add.html'
    model = Tracker
    fields = ['summary', 'description', 'type', 'status']
    success_url = reverse_lazy('index')
    permission_required = 'webapp.change_tracker'

    def form_valid(self, form):
        form.instance.project_id = self.kwargs['pk']
        return super().form_valid(form)


class TrackerUpdateView(LoginRequiredMixin, UpdateView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'tracker/tracker_update.html'
    permission_required = 'webapp.change_tracker'

    def get_success_url(self):
        return reverse('tracker_view', kwargs={'pk': self.object.pk})


class DeleteTrackerView(LoginRequiredMixin, DeleteView):
    template_name = 'tracker/tracker_delete.html'
    model = Tracker
    success_url = reverse_lazy('index')
    permission_required = 'webapp.change_project'


class ProjectView(LoginRequiredMixin, ListView):
    template_name = 'project/index.html'
    model = Project
    context_object_name = 'projects'
    permission_required = 'webapp.change_project'

    # PermissionRequiredMixin,


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_detail.html'
    permission_required = 'webapp.change_project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trackers'] = Tracker.objects.filter(project=self.object)
        return context


class ProjectAdd(LoginRequiredMixin, CreateView):
    template_name = 'project/project_add.html'
    model = Project
    fields = ['start_date', 'end_date', 'name', 'description']
    success_url = reverse_lazy('index')
    permission_required = 'webapp.change_project'


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_update.html'
    permission_required = 'webapp.change_project'

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    template_name = 'project/project_delete.html'
    model = Project
    success_url = reverse_lazy('project_index')

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=False)
        return queryset
