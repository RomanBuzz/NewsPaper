from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['post_title', 'post_text', 'post_category']

    def clean(self):
        cleaned_data = super().clean()
        post_title = cleaned_data.get("post_title")
        post_text = cleaned_data.get("post_text")

        if len(str(post_text)) < 20:
            raise ValidationError(
                "Содержание публикации не должно быть короче 20 символов."
            )

        if post_title == post_text:
            raise ValidationError(
                "Содержание публикации не должно быть идентично названию."
            )

        return cleaned_data
