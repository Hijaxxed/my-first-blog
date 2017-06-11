from django import forms

from pagedown.widgets import PagedownWidget

from .models import Post, Comment

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=PagedownWidget)
    class Meta:
        model = Post
        fields = (
            'title',
            #'categories',
            'text',
            'image'
            )
        
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
