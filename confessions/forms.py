from django import forms

from .models import ConfessionRequest, ConfessionReport

class ConfessionForm(forms.ModelForm):
    class Meta:
        model = ConfessionRequest
        fields = {'content'}

class ConfessionReportForm(forms.ModelForm):
    class Meta:
        model = ConfessionReport
        fields = {'reason'}