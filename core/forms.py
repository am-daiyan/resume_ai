from django import forms
from .models import details,resume

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

# class contact_form(forms.ModelForm):
#     PASS
