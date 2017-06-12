from django import forms

from pagedown.widgets import PagedownWidget

from .models import Post, Comment  #Category

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=PagedownWidget)
    #category = Category.title()
    class Meta:
        model = Post
        fields = (
            'title',
            #'category',
            'text',
            'image'
            )
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
