"""Detection forms."""

# Django
from django import forms

# Models
from detections.models import Detection, Note

class NoteForm(forms.ModelForm):
    """Note model form."""
    class Meta:
        """Form settings."""
        model = Note
        fields = ('name', 'text')
