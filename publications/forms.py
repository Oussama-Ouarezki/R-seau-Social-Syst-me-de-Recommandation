from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'interests']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Quoi de neuf ?'}),
            'interests': forms.CheckboxSelectMultiple(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Votre commentaire...'}),
        }
