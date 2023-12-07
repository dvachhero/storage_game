from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import QuestionStorageGame, AnswerStorageGame, QuestionStorageGameTraining, AnswerStorageGameTraining
from django.db.models import F
import random
from random import choice, shuffle


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

#ДЛЯ ТРЕНИРОВКИ

def get_random_question():
    questions = list(QuestionStorageGameTraining.objects.all())
    return choice(questions) if questions else None

def get_shuffled_answers(question):
    answers = [question.answer1, question.answer2, question.answer3, question.answer4]
    shuffle(answers)
    return answers

@login_required(login_url='/login/')
def GameTrainingView(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_answer = request.POST.get('answer')
        question = get_object_or_404(QuestionStorageGameTraining, id=question_id)

        correct = selected_answer == question.answer1

        user_answer, created = AnswerStorageGameTraining.objects.get_or_create(
            user=request.user,
            question=question,
        )

        if correct:
            user_answer.correct_answers_training += 1
            user_answer.save()


        # Перенаправляем пользователя на следующий вопрос
        return redirect('gametraining')

    question = get_random_question()
    if not question:
        return render(request, 'no_questions.html')  # Представление, если нет вопросов

    answers = get_shuffled_answers(question)
    return render(request, 'gametraining.html', {'question': question, 'answers': answers})

@login_required(login_url='/login/')
def ResultInfoTrainingView(request):
    correct_answers = request.session.get('correct_answers_training', 0)
    # Здесь можно добавить логику для записи лучшего результата пользователя
    request.session['correct_answers'] = 0  # Сбросить счетчик
    return render(request, 'resultinfotraining.html', {'correct_answers_training': correct_answers})


