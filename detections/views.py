"""Detections views."""
# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# Models
from detections.models import Detection, Note

# Forms
from detections.forms import NoteForm

# My classes
from .manage import ManageDetections, ManageNewDetection

# MyApps
from sugar.app import CalculateVi, MakeCloustering
from sugar.savefiles import SaveFile,SaveDetection

# Other
from datetime import datetime, timedelta

class IndexView(LoginRequiredMixin, ListView):
    """Return Index."""
    template_name = 'detections/index.html'
    model = Detection

    def get_context_data(self, **kwargs):
        #https://canvasjs.com/javascript-range-area-spline-area-chart/
        context = super().get_context_data(**kwargs)
        last_month = datetime.today() - timedelta(days=14)
        detections_month = Detection.objects.filter(created__gte=last_month).order_by('created')
        detections_m = ""
        detections_m_name = ""
        detections_m_date = ""

        for detection in detections_month:
            detections_m = detections_m+";"+str(detection.water_stress_percent)
            detections_m_name=detections_m_name+";"+str(detection.name)
            detections_m_date = detections_m_date+";"+str(detection.created)

        context['detections_stress'] = detections_m
        context['detections_name'] = detections_m_name
        context['detections_date'] = detections_m_date
        context['detections'] = Detection.objects.all().order_by('-created')
        context['v'] = 'some-string'

        return context


class AllDetectionsView(LoginRequiredMixin, ListView):
    """Return detections."""
    template_name = 'detections/all.html'
    model = Detection
    ordering = ('-created',)
    #paginate_by = 5
    context_object_name = 'detections'

class NewDetectionView(LoginRequiredMixin, TemplateView):
    """New detection view."""
    template_name = "detections/new.html"

    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return ManageNewDetection(self, request, *args, **kwargs)


class NoteReadView(LoginRequiredMixin, DetailView):
    """Detail note view."""
    model = Note
    template_name = 'detections/crud/read_note.html'
    context_object_name = 'note'
    form_class = NoteForm

class NoteDeleteView(LoginRequiredMixin, DetailView):
    """Delete note view."""
    model = Note
    template_name = 'detections/crud/delete_note.html'
    context_object_name = 'note'

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            pk = request.POST['note_pk']
            note_instance = Note.objects.get(pk=pk)
            detection_name = note_instance.note_detection.name
            note_instance.delete()
            return redirect('detections:detection_detail', name=detection_name)

class NoteEditView(LoginRequiredMixin, UpdateView):
    """Update note view."""
    model = Note
    form_class = NoteForm
    template_name = 'detections/crud/edit_note.html'
    context_object_name = 'note'

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        note = self.get_object()
        detection_name = note.note_detection.name
        return reverse_lazy('detections:detection_detail', kwargs={'name': detection_name})


class DetectionDetailView(LoginRequiredMixin, DetailView):
    """Detection detail view."""
    template_name = 'detections/detail.html'
    slug_field = 'name'
    slug_url_kwarg = 'name'
    model = Detection
    context_object_name = 'detection'

    def post(self, request, *args, **kwargs):
        return  ManageDetections(self, request, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(DetectionDetailView, self).__init__(*args, **kwargs)
        self.object_list = self.get_queryset()

    def get_context_data(self, **kwargs):
        """Add detection's notes to context."""
        context = super().get_context_data(**kwargs)
        detection = self.get_object()
        context['notes'] = Note.objects.filter(note_detection=detection).order_by('-created')
        context['detections'] = Detection.objects.all().order_by('-created')
        return context

class LastDetectionView(LoginRequiredMixin, DetailView):
    """Last detection view."""
    template_name = 'detections/detail.html'
    model = Detection
    context_object_name = 'detection'

    def post(self, request, *args, **kwargs):
        return ManageDetections(self, request, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(LastDetectionView, self).__init__(*args, **kwargs)
        self.object_list = self.get_queryset()

    def get_object(self, queryset=None):
        object_instance = Detection.objects.all().order_by('-created').first()
        return object_instance

    def get_context_data(self, **kwargs):
        """Add detection's notes to context."""
        context = super().get_context_data(**kwargs)
        detection = self.get_object()
        context['notes'] = Note.objects.filter(note_detection=detection).order_by('-created')
        context['detections'] = Detection.objects.all().order_by('-created')
        return context
