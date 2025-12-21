from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout
from .models import details,resume,ContactMessage
from .forms import student_details,resume_upload,ContactForm
from .utils import extract_text
from .ai_prompts import SYSTEM_PROMPT, USER_TEMPLATE
import requests
from django.http import JsonResponse
import os
from django.core.mail import send_mail
from django.conf import settings
import markdown

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

def about(request):
    return render(request,"about.html")

def privacy_policy(request):
    return render(request,"Privacy_Policy.html")

def terms(request):
    return render(request,"terms&condition.html")

def FAQs(request):
    return render(request,"FAQs.html")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Account created successfully! Welcome.")
            return redirect('home')
    else:
        form = UserCreationForm()
        # FIX: Apply Bootstrap class to fields
        for field in form.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        # FIX: Apply Bootstrap class to fields
        for field in form.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

def preview(request, id):
    prev = resume.objects.get(id=id)
    pdf_url = prev.resume_file.url
    extracted_text = extract_text(prev.resume_file.path)
    ai_output = None

    if request.method == "POST":
        user_prompt = USER_TEMPLATE["content"].format(
            resume_text=extracted_text
        )

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY', '')}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "deepseek/deepseek-r1-0528:free",
            "max_tokens": 8000,
            "messages": [
                SYSTEM_PROMPT,
                {"role": "user", "content": user_prompt},
            ],
        }

        resp = requests.post(url, headers=headers, json=data)

        try:
            res_json = resp.json()
        except Exception:
            ai_output = "AI returned an invalid response."
        else:
            if resp.status_code != 200:
                ai_output = f"AI API Error ({resp.status_code}): {res_json}"
            elif "choices" not in res_json:
                ai_output = f"Unexpected AI response: {res_json}"
            else:
                raw_output = res_json["choices"][0]["message"]["content"]
                ai_output = markdown.markdown(
                    raw_output,
                    extensions=["extra"]
                )

    return render(
        request,
        "preview.html",
        {
            "pdf_url": pdf_url,   # used by iframe
            "ai_output": ai_output
        }
    )



def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            send_mail(
                subject=f"New Contact Message: {contact.subject}",
                message=f"""
        Name: {contact.name}
        Email: {contact.email}

        Message:
        {contact.message}
        """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['daiyanali551@gmail.com'],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact_us')
    # Redirect to prevent resubmission
    else:
        form = ContactForm()

    # We can fetch developer info here if needed, but keeping it simple for now.
    developer_info = {
        'email': 'daiyanali551@gmail.com',  # Placeholder
        'github': 'Daiyan Ali Abbas',
        'location': 'India',
    }

    return render(request, "contact-us.html", {'form': form, 'developer_info': developer_info})

def resume_builder(request):
    return render(request, "resume_builder.html")

