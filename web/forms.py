from django import forms

class PostForm(forms.Form):
    bname = forms.CharField(max_length=20, required=True,initial='')
    bemail = forms.EmailField(max_length=100, required=True, initial='')
    bphoneNum = forms.CharField(max_length=20, required=True, initial='')
    bcontent = forms.CharField(required=True, widget=forms.Textarea)