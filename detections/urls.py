"""Detections URLs."""

# Django
from django.urls import path

# View
from detections import views

urlpatterns = [
        # Management
    path(
        route='',
        view=views.IndexView.as_view(),
        name='home'
    ),
    path(
        route='new-detection/',
        view=views.NewDetectionView.as_view(),
        name='new_detection'
    ),
    path(
        route='detections/',
        view=views.AllDetectionsView.as_view(),
        name='all_detections',
    ),
    path(
        route='last_detection/',  # Detection Management
        view=views.LastDetectionView.as_view(),
        name='last_detection'
    ),
    path(
        route='<str:name>/',  # Detection Management
        view=views.DetectionDetailView.as_view(),
        name='detection_detail'
    ),
    path(
        route='read/<int:pk>',
        view=views.NoteReadView.as_view(),
        name='read_note'
    ),
    path(
        route='delete/<int:pk>',
        view=views.NoteDeleteView.as_view(),
        name='delete_note'
    ),
    path(
        route='edit/<int:pk>',
        view=views.NoteEditView.as_view(),
        name='edit_note'
    ),
]
