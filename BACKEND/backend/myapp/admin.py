from django.contrib import admin
from .models import Submission, PlagiarismResult

admin.site.register(Submission)
admin.site.register(PlagiarismResult)
