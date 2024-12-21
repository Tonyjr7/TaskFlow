from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Task(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField()
    priority = models.IntegerField(choices=((1, 'Low'), (2, 'Medium'), (3, 'High')))
    completed = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField()


    def __str__(self):
        return self.title
    