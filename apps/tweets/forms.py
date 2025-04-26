from django import forms
from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg',
                'placeholder': '¿Qué está pasando? (máx. 280 caracteres)',
                'maxlength': '280',
                'rows': '3'
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 280:
            raise forms.ValidationError("El tweet no puede exceder los 280 caracteres.")
        return content