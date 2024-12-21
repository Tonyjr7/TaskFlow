from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account, Task

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if not email:
                raise forms.ValidationError('Email is required.')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Email address already registered.')
            return email
        
        def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']  # Explicitly assign email
            useremail = self.cleaned_data['email']
            if commit:
                user.save()
                # Account.objects.create(
                #     user=user,
                #     email = "ha@gmail.com",
                # )
                # Account.save()
            return user
        
class CreateTaskForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    PRIORITY_CHOICES = (
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High'),
    )
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES)
    completed = forms.BooleanField(required=False)
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'completed']

    def save(self, commit=True):
        task = super().save(commit=False)
        # Add any custom logic here if needed
        if commit:
            task.save()
        return task

class UpdateTaskForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    PRIORITY_CHOICES = (
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High'),
    )
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES)
    completed = forms.BooleanField(required=False)
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'completed', 'due_date']




        