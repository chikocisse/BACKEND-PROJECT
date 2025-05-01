from django import forms

class UploadForm(forms.Form):
    file = forms.FileField(label="Upload a file")

class PlagiarismForm(forms.Form):
    file = forms.FileField(label='Upload a file for plagiarism check')
