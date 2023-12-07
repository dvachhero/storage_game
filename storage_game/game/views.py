from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import QuestionStorageGame, AnswerStorageGame
from django.db.models import F
import random

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
def play(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def result(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def rules(request):
    return render(request, 'rules.html')

@login_required(login_url='/login/')
def game(request):
    question = QuestionStorageGame.objects.filter(
        id__gt=request.user.profile.last_question_id).first()

    if question is None:
        answers = AnswerStorageGame.objects.filter(
            user=request.user, right_answer=F('answer')).count()
        return redirect('resultinfo')

    if request.method == "POST":
        selected_answer = request.POST.get('answer')
        question_id = request.POST.get('question_id')
        question = get_object_or_404(QuestionStorageGame, pk=question_id)

        existing_answer = AnswerStorageGame.objects.filter(
            user=request.user, question=question).first()

        if existing_answer:
            existing_answer.answer = selected_answer
            existing_answer.save()
        else:
            AnswerStorageGame.objects.create(
                user=request.user,
                question=question,
                answer=selected_answer,
                right_answer=question.answer1
            )

        request.user.profile.last_question_id = question.id
        request.user.profile.save()
        return redirect('game')
    answers = [question.answer1, question.answer2, question.answer3, question.answer4]
    random.shuffle(answers)
    return render(request, 'game.html', {'question': question, 'answers': answers})



@login_required(login_url='/login/')
def resultinfo(request):
    user = request.user

    correct_answers = AnswerStorageGame.objects.filter(
        user=user, right_answer=F('answer')).count()

    total_questions = QuestionStorageGame.objects.count()
    return render(request, 'resultinfo.html', {'correct_answers': correct_answers, 'total_questions': total_questions})

@login_required(login_url='/login/')
def user_results(request):
    user_answers = AnswerStorageGame.objects.filter(user=request.user)
    return render(request, 'user_results.html', {'user_answers': user_answers})

@login_required(login_url='/login/')
def game_menu(request):
    return render(request, 'gamemenu.html')


