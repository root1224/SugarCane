"""Manage detections views."""
# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.shortcuts import render

# Models
from detections.models import Detection, Note

# MyApps
from sugar.app import CalculateVi, MakeCloustering
from sugar.savefiles import SaveFile,SaveDetection

import random

def ManageDetections(self, request, *args, **kwargs):
    """Manage detections."""
    self.object = self.get_object()
    context = self.get_context_data()
    if 'cloustering_ndvi' in request.POST:
        detection = self.get_object()
        if int(request.POST['n_clouster_ndvi']) != 0:
            number = request.POST['n_clouster_ndvi']
            type_vi = 'ndvi'
            picture_url = detection.picture_ndvi.url

            MakeCloustering(request.user,int(number),picture_url)
            context['done_clouster'] = type_vi

    elif 'cloustering_savi' in request.POST:
        detection = self.get_object()
        if int(request.POST['n_clouster_savi']) != 0:
            number = request.POST['n_clouster_savi']
            type_vi = 'savi'
            picture_url = detection.picture_savi.url

            MakeCloustering(request.user,int(number),picture_url)
            context['done_clouster'] = type_vi

    elif 'cloustering_evi2' in request.POST:
        detection = self.get_object()
        if int(request.POST['n_clouster_evi2']) != 0:
            number = request.POST['n_clouster_evi2']
            type_vi = 'evi2'
            picture_url = detection.picture_evi2.url

            MakeCloustering(request.user,int(number),picture_url)
            context['done_clouster'] = type_vi

    elif 'savenote' in request.POST:
        user = request.user
        detection = self.get_object()
        name = request.POST['note_name']
        text = request.POST['note-text']
        new_note = Note(note_detection=detection, name=name, user=user, text=text)
        new_note.save()

    return render(request, 'detections/detail.html', context)


def ManageNewDetection(self, request, *args, **kwargs):
    """Manage new detection."""
    if 'detect' in request.POST:
        files_detection = request.FILES.getlist('files')
        if files_detection:
            if len(files_detection) == 5:
                extention = []
                if not any("RGB" in s.name for s in files_detection):
                    extention.append("RGB")
                if not any("NIR" in s.name for s in files_detection):
                    extention.append("NIR")
                if not any("RED" in s.name for s in files_detection):
                    extention.append("RED")
                if not any("REG" in s.name for s in files_detection):
                    extention.append("REG")
                if not any("GRE" in s.name for s in files_detection):
                    extention.append("GRE")

                if not extention:
                    for request_file in files_detection:
                        SaveFile(request_file, request.user.username)

                    state,water_stress_percent,water_stress = CalculateVi(request.user.username)

                    context = {
                        'save_detect' : True,
                        'state' : state,
                        'percent' : water_stress_percent,
                        'stress' : water_stress
                        }
                else:
                    context = { 'msg' : 'Select files: '+','.join([str(n) for n in extention]) }
            else:
                context = {
                    'msg' : 'Select five files.'
                }
        else:
            context = {
                'msg' : 'Select files.'
            }
        return render(request, self.template_name, context)

    elif 'save' in request.POST:
        user = request.user
        profile = request.user.profile
        detection_name = request.POST["name"]
        status = request.POST["satatus_of_field"]
        water_stress_percent = request.POST["percent_stress"]
        water_stress = request.POST["water_stress"]

        if request.POST['note_name'] and request.POST['note_text']:
            note_name = request.POST['note_name']
            note_text = request.POST['note_text']
            SaveDetection(
                request=request,
                user=user,
                profile=profile,
                detection_name=detection_name,
                status=status,
                water_stress=water_stress,
                water_stress_percent=water_stress_percent,
                note_name=note_name,
                note_text=note_text
            )
        else:
            SaveDetection(
                request=request,
                user=user,
                profile=profile,
                detection_name=detection_name,
                status=status,
                water_stress=water_stress,
                water_stress_percent=water_stress_percent,
                note_name=None,
                note_text=None
            )
        return redirect('detections:last_detection')

    return render(request, self.template_name)
