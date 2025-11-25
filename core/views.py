from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import details,resume
from .forms import student_details,resume_upload
from .utils import extract_text
from .ai_prompts import SYSTEM_PROMPT, USER_TEMPLATE
import requests
from django.http import JsonResponse
import os

import json
# Create your views here.
def home(request):
    if request.method=="POST":
        form=resume_upload(request.POST,request.FILES)
        if form.is_valid():
            prev=form.save()
            return redirect('preview',id=prev.id)
    else:
        form=resume_upload()
    return render(request,"index.html",{'form':form})

def rough(requests):
    return render(requests,"rough.html")

def about(request):
    return render(request,"about.html")

def contact_us(request):
    return render(request,"contact-us.html")

def privacy_policy(request):
    return render(request,"Privacy_Policy.html")

def terms(request):
    return render(request,"terms&condition.html")

def FAQs(request):
    return render(request,"FAQs.html")

def preview(request,id):
    prev=resume.objects.get(id=id)
    file_path=prev.resume_file.path
    extracted_text=extract_text(file_path)
    ai_output=None

    if request.method=="POST":
        user_prompt=USER_TEMPLATE["content"].format(resume_text=extracted_text)

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY','')}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "google/gemma-3-27b-it:free",
            "max_tokens":8000,
            "messages": [
                SYSTEM_PROMPT,
                {"role": "user", "content": user_prompt}
            ]
        }

        resp = requests.post(url, headers=headers, json=data)
        res_json = resp.json()
        if "choices" in res_json:
            ai_output = res_json["choices"][0]["message"]["content"]
        else:
            ai_output = "Error: Could not get AI response"
    return render(request, "preview.html", {
        "text": extracted_text,
        "ai_output": ai_output
    })

def list(request):
    if request.method=="POST":
        form=student_details(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Student added successfully.")
            return redirect('student_d')
    else:
        form=student_details()
    return render(request,'student_list.html',{'form':form})

def student_d(requests):
    form=details.objects.all()
    return render(requests,"student_details.html",{'form':form})


