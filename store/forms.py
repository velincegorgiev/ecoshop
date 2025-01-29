from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(label="Enter Comment", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'text', 'id': 'form-comment'}))

    class Meta:
        model = Comment
        fields = ['text']
