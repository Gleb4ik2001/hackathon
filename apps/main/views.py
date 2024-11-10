from django.shortcuts import render
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .chatgpt_filter import filter_resumes_with_chatgpt
from .extract_resume_text import extract_resume_text


@method_decorator(login_required, name='dispatch')  # Применение декоратора login_required ко всем методам класса
class MainView(View):
    template_name = 'main.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        files = request.FILES.getlist('folder')
        position = request.POST.get('position')
        experience = request.POST.get('experience')

        if not position or not experience:
            return render(request, self.template_name, {"error": "Пожалуйста, укажите должность и опыт работы."})

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        resumes_data = []

        for file in files:
            file_path = fs.save(file.name, file)
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            text = extract_resume_text(full_path)
            resumes_data.append({
                "file_name": file.name,
                "text": text
            })

        suitable_resumes = filter_resumes_with_chatgpt(resumes_data, position, experience)

        context = {"suitable_resumes": suitable_resumes}
        return render(request, self.template_name, context)
