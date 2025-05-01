from django.shortcuts import render
from django.http import JsonResponse
from .models import Submission
from .forms import UploadForm  



def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        
        # Save the file (you can modify this based on your model)
        submission = Submission(file=uploaded_file)
        submission.save()

        # Trigger automatic correction and plagiarism check
        # (If necessary, you can call the correction and plagiarism functions here)
        return JsonResponse({'message': 'File uploaded successfully', 'submission_id': submission.id})
    else:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
