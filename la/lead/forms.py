from django import forms
from .models import Lead, Comment, LeadFile

WIDGET_ATTRS = {"class": "w-full py-4 px-6 rounded-xl bg-gray-100 mb-2"}

class AddLeadForm(forms.ModelForm):
    name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs=WIDGET_ATTRS),
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.TextInput(attrs=WIDGET_ATTRS),
    )
    description = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={"rows": "5", "class": "mb-2 w-full bg-gray-100 rounded-xl"}),
    )
    priority = forms.ChoiceField(
        label="Prioridad",
        choices=Lead.CHOICES_PRIORITY,
        widget=forms.Select(attrs=WIDGET_ATTRS),
    )
    status = forms.ChoiceField(
        label="Estado",
        choices=Lead.CHOICES_STATUS,
        widget=forms.Select(attrs=WIDGET_ATTRS),
    )

    class Meta:
        model = Lead
        fields = ("name", "email", "description", "priority", "status")

class AddCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "5", "class": "w-full bg-gray-100 rounded-xl"}))

    class Meta:
        model = Comment
        fields = ['content']

class AddFileForm(forms.ModelForm):
    class Meta:
        model = LeadFile
        fields = ('file',)
