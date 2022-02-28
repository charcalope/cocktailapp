from django import forms

class CreateBlogPostForm(forms.Form):
    title = forms.CharField(max_length=200)
    photo = forms.URLField()
    content = forms.CharField(widget=forms.Textarea)
