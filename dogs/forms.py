import datetime

from django import forms

from dogs.models import Dog, Parent
from users.forms import StyleFormMixin


class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        exclude = ('owner', 'is_active', 'views')

    def clean_birth_date(self):  # функция проверяет чтобы возраст собаки был моложе 100 лет
        if self.cleaned_data['birth_date']:
            cleaned_data = self.cleaned_data['birth_date']  # выбрать введеную дату рождение собаки из формы
            now_year = datetime.datetime.now().year  # выбрать текущую дату
            if now_year - cleaned_data.year > 100:  # если текущий год минус год рождения больше чем 100 вызвать ошибку
                raise forms.ValidationError('Собака должна быть моложе 100 лет')
            return cleaned_data
        return


class DogAdminForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'

    def clean_birth_date(self):  # функция проверяет чтобы возраст собаки был моложе 100 лет
        if self.cleaned_data['birth_date']:
            cleaned_data = self.cleaned_data['birth_date']  # выбрать введеную дату рождение собаки из формы
            now_year = datetime.datetime.now().year  # выбрать текущую дату
            if now_year - cleaned_data.year > 100:  # если текущий год минус год рождения больше чем 100 вызвать ошибку
                raise forms.ValidationError('Собака должна быть моложе 100 лет')
            return cleaned_data
        return


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
