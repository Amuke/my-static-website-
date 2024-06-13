# polls/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Choice

def index(request):
    """
    Display the latest 5 poll questions.
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

@login_required
def detail(request, question_id):
    """
    Display the details of a specific poll question.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

@login_required
def results(request, question_id):
    """
    Display the results of a specific poll question.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required
def vote(request, question_id):
    """
    Handle voting on a poll question.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # If choice doesn't exist or no choice was made
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Update the vote count for the selected choice
        selected_choice.votes += 1
        selected_choice.save()
        # Redirect to the results page after voting
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def user_login(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        # Authenticate user with provided credentials
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:index')
        else:
            # If authentication fails, show an error message
            return render(request, 'polls/login.html', {'error_message': 'Invalid credentials'})
    else:
        return render(request, 'polls/login.html')

def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:login')
    else:
        form = UserCreationForm()
    return render(request, 'polls/register.html', {'form': form})

def user_logout(request):
    """
    Handle user logout.
    """
    logout(request)
    return redirect('polls:login')
