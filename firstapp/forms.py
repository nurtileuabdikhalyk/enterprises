from datetime import datetime

from django.contrib.auth.forms import UserCreationForm

from .models import *
from django import forms


class NotesForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(NotesForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['organization'] = forms.ModelChoiceField(
            queryset=User.objects.filter(username=self.user), initial=True,
            widget=forms.Select(attrs={"class": "form-control", }, ))

    class Meta:
        model = Notes
        fields = ('organization', 'title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control", "cols": 20, "rows": 2, })
        }


class SignInForm(forms.ModelForm):
    login = forms.CharField(label='Логин',
                            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Логин"}))
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Құпия сөз"}))

    class Meta:
        model = User
        fields = ('login', 'password',)


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={"class": "form-control", }))
    password1 = forms.CharField(label='Құпия сөз',
                                widget=forms.PasswordInput(attrs={"class": "form-control", }))
    password2 = forms.CharField(label='Құпия сөзді қайталаңыз',
                                widget=forms.PasswordInput(
                                    attrs={"class": "form-control", }))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',
                  )


class ProductForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['organization'] = forms.ModelChoiceField(
            queryset=User.objects.filter(username=self.user), initial=True,
            widget=forms.Select(attrs={"class": "form-control", }, ))

    class Meta:
        model = Product
        fields = ('organization', 'name', 'price', 'count', 'place')
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'price': forms.NumberInput(attrs={"class": "form-control"}),
            'count': forms.NumberInput(attrs={"class": "form-control"}),

            'place': forms.TextInput(attrs={"class": "form-control"}),
        }


class OrderForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['organization'] = forms.ModelChoiceField(
            queryset=User.objects.filter(username=self.user), initial=True,
            widget=forms.Select(attrs={"class": "form-control", }, ))
        self.fields['platej'] = forms.ModelChoiceField(
            queryset=Platej.objects.filter(organization=self.user), initial=True,
            widget=forms.Select(attrs={"class": "form-control", }, ))

        self.fields['courier'] = forms.ModelChoiceField(
            queryset=Courier.objects.filter(organization=self.user), initial=True,
            widget=forms.Select(attrs={"class": "form-control", }, ))

    class Meta:
        model = Order
        fields = ('organization', 'data', 'platej', 'courier',)
        widgets = {
            'data': forms.DateTimeInput(attrs={"class": "form-control", 'type': 'datetime-local'}),

        }


class PlatejForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(PlatejForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['organization'] = forms.ModelChoiceField(
            queryset=User.objects.filter(username=self.user), initial=True,
            widget=forms.Select(attrs={"class": "form-control", }, ))

        self.fields['dogovor'] = forms.ModelChoiceField(
            queryset=Dogovor.objects.all(), initial=True,
            widget=forms.Select(attrs={"class": "form-control", }, ))

        self.fields['product'] = forms.ModelChoiceField(
            queryset=Product.objects.filter(count__gte=1).filter(organization=self.user), initial=True,
            widget=forms.Select(attrs={"class": "form-control", }, ))

    class Meta:
        model = Platej
        fields = ('organization', 'dogovor', 'product', 'sum', 'oplata', 'address', 'count', 'status')
        widgets = {
            'dogovor': forms.TextInput(attrs={"class": "form-control", }),
            'project': forms.TextInput(attrs={"class": "form-control", }),
            'address': forms.TextInput(attrs={"class": "form-control", }),
            'oplata': forms.Select(attrs={"class": "form-control", }),
            'status': forms.Select(attrs={"class": "form-control", }),
            'count': forms.NumberInput(attrs={"class": "form-control", }),
            'sum': forms.NumberInput(attrs={"class": "form-control", }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'subject', 'message')
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control", }),
            'last_name': forms.TextInput(attrs={"class": "form-control", }),
            'email': forms.EmailInput(attrs={"class": "form-control", }),
            'subject': forms.TextInput(attrs={"class": "form-control", }),
            'message': forms.Textarea(
                attrs={"class": "form-control", "placeholder": ". . .", "cols": 30, "rows": 7, }),
        }


class CourierForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(CourierForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['organization'] = forms.ModelChoiceField(
            queryset=User.objects.filter(username=self.user), initial=True,
            widget=forms.Select(attrs={"class": "form-control", }, ))

    class Meta:
        model = Courier
        fields = ('organization', 'first_name', 'last_name', 'phone')
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control", }),
            'last_name': forms.TextInput(attrs={"class": "form-control", }),
            'phone': forms.TextInput(attrs={"class": "form-control", }),

        }


