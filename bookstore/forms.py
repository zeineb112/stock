from bootstrap_modal_forms.mixins import CreateUpdateAjaxMixin, PopRequestMixin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from bookstore.models import Book


class YourForm(forms.Form):
    controle = forms.CharField(widget=forms.Select(choices=[('urgent', 'Urgent'), ('Normal', 'Normal')]))
class YourForm1(forms.Form):
    conforme = forms.CharField(widget=forms.Select(choices=[('Non conforme', 'Non conforme'), ('conforme', 'conforme')]))
        
class BookForm(forms.Form):
    class Meta:
        model = Book
        fields = ('controle',)  

class BookForm1(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title','year','author','desc','Nands','publisher')  
        labels = {
            'title':' Product Name',
            'year': 'Remaining product quantity of last day',
            'author': 'Product quantity for today',
            'desc' : 'Replenished product',
            'Nands':"Today's product usage",
            'publisher':'product quantity found'
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')