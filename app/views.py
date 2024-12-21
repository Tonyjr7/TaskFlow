from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Account, Task
from .forms import SignUpForm, CreateTaskForm,UpdateTaskForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import logout

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            Account.objects.create(user=user, email=email, first_name=first_name, last_name=last_name)
        return redirect('signup_successful')
    else:
        form = SignUpForm()
    
    return render(request, 'app/signup.html', {'form': form})
@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')


def signup_successful(request):
    return render(request, 'app/signup_successful.html')

@login_required
def redirect_after_login(request):
    try:
        account = Account.objects.get(user=request.user)
        return redirect('dashboard', account_id=account.id)
    except Account.DoesNotExist:
        return redirect('signup')


@login_required
def dashboard(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    data = Task.objects.filter(account_id=account.id)
    if data.exists():
        HttpResponse("Task already exists")
    else:
        HttpResponse("Task does not exist, creating new one")

    return render(request, 'app/dashboard.html', {'data': data, 'account': account})

@login_required
def TaskDetailView(request, account_id, pk):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    task = get_object_or_404(Task, id=pk, account_id=account.id)
    return render(request, 'app/task_detail.html', {'task': task, 'account': account})

@login_required
def CreateTaskView(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # Create a Task instance without saving yet
            task.account = account  # Associate the Task with the Account
            task.save()  # Save the Task to the database
            #send task email notification
            def send_task_email(account, task):

                email_content = render_to_string('app/task_creation_confirmation.html', {
                    "task": task,
                    "account": account,
                })

                send_mail(
                    subject='Task Created Successfully',
                    message='',  # Plain text fallback can be left empty
                    html_message=email_content,  # Use rendered HTML content
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[account.email],
                )
            send_task_email(account, task)
            return redirect('dashboard', account_id=account.id)
    else:
        form = CreateTaskForm()

    return render(request, 'app/add_task.html', {'account_id': account_id, 'form': form})

@login_required
def DeleteTaskView(request, account_id, pk):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    task = get_object_or_404(Task, id=pk, account_id=account.id)
    if request.method == 'POST':
        task.delete()

        def delete_task_email(account, task):
            email_content = render_to_string('app/task_deletion_confirmation.html', {
                "task": task,
                "account": account,
            })

            send_mail(
                subject='Task Deleted Successfully',
                message='',  # Plain text fallback can be left empty
                html_message=email_content,  # Use rendered HTML content
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[account.email],
            )
        delete_task_email(account, task)

        return redirect('dashboard', account_id=account.id)
    
    return render(request, 'app/delete_task.html', {'id' : task, 'account': account})

@login_required
def UpdateTaskView(request, account_id, pk):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    task = get_object_or_404(Task, id=pk, account_id=account.id)
    if request.method == 'POST':
        form = UpdateTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            due_date = form.cleaned_data['due_date']
            priority = form.cleaned_data['priority']
            completed = form.cleaned_data['completed']
            description = form.cleaned_data['description']
            task.due_date = due_date
            task.priority = priority
            task.completed = completed
            task.description = description
            task.title = title
            task.save()

            # def update_task_email(account, task):

            #     email_content = render_to_string('app/task_update_confirmation.html', {
            #         "task": task,
            #         "account": account,
            #     })

            #     send_mail(
            #         subject='Task Updated Successfully',
            #         message='',  # Plain text fallback can be left empty
            #         html_message=email_content,  # Use rendered HTML content
            #         from_email=settings.EMAIL_HOST_USER,
            #         recipient_list=[account.email],
            #     )

            # update_task_email(account, task)

            return redirect('dashboard', account_id=account.id)
    elif request.method == 'GET':
        form = UpdateTaskForm(instance=task)
    
    return render(request, 'app/edit_task.html', {'account': account, 'form': form, 'id': task})