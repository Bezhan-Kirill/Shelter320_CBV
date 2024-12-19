from django import forms
import datetime
from dogs.models import Dog
from users.forms import StyleFormMixin


# class DogForm(StyleFormMixin, forms.ModelForm):
#     class Meta:
#         model = Dog
#         fields = '__all__'

class DogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        exclude = ('owner',)

    def clean_birth_date(self):
        cleaned_data = self.cleaned_data['birth_date']
        now_year =datetime.datetime.now().year
        if now_year - cleaned_data.year > 100:
            raise forms.ValidationError('Собака должна быть моложе 100 лет')
# class DogUpdateForm(StyleFormMixin, forms.ModelForm):
#     class Meta:
#         model = Dog
#         exclude = ('owner',)