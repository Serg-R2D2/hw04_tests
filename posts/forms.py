from django import forms
from .models import Post


class PostForm(forms.ModelForm): 
    class Meta:                                                           
        model = Post                                                      
        fields = ('text', 'group', 'image') 
        labels = {                 
            'text': 'Текст',       
            'group': 'Сообщество',
            'image': 'Картинка'
            }
        help_text = {
            'text': 'Hапишите свой пост здесь',
            'group': 'Выберите сообщество'
            }
