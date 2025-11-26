from django import forms
from .models import details,resume,ContactMessage

class student_details(forms.ModelForm):
    class Meta:
        model=details
        fields=["name","roll_no"]

class resume_upload(forms.ModelForm):
    class Meta:
        model=resume
        fields=['resume_file']
        labels={'resume_file':''}
        widgets ={
            'resume_file':forms.ClearableFileInput(attrs={
                'accept': '.pdf,.docx',
                'id': 'fileInput',
                'style': 'display:none',
                'onchange': 'this.form.submit();'
            })
        }

# New Form for Contact Messages
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Message'}),
        }
