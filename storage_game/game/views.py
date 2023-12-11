from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import QuestionStorageGame, AnswerStorageGame, QuestionTraining, AnswerTraining, KmbAnswerStorage, KmbQuestionStorage, UserResultsAccess, UserResultsKmbAccess
from django.db.models import F
import random
from django.urls import reverse
from django.http import HttpResponseRedirect


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def play(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def result(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def rules(request):
    return render(request, 'rules.html')

@login_required(login_url='login')
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



@login_required(login_url='login')
def resultinfo(request):
    user = request.user

    correct_answers = AnswerStorageGame.objects.filter(
        user=user, right_answer=F('answer')).count()

    total_questions = QuestionStorageGame.objects.count()
    return render(request, 'resultinfo.html', {'correct_answers': correct_answers, 'total_questions': total_questions})

@login_required(login_url='login')
def user_results(request):
    if not UserResultsAccess.objects.first().is_access_enabled:
        return redirect('/gamemenu')  # Перенаправьте пользователя на другую страницу

    user_answers = AnswerStorageGame.objects.filter(user=request.user)
    return render(request, 'user_results.html', {'user_answers': user_answers})
@login_required(login_url='login')
def game_menu(request):
    return render(request, 'gamemenu.html')

#Для тренировки
def game_training(request):
    # Инициализируем текущую серию правильных ответов
    if 'current_sequence' not in request.session:
        request.session['current_sequence'] = 0

    if request.method == 'POST':
        selected_answer = request.POST.get('answer')
        question_id = request.POST.get('question_id')
        question = get_object_or_404(QuestionTraining, pk=question_id)

        # Проверяем правильность ответа
        is_correct = (selected_answer == question.answer_1)

        if is_correct:
            request.session['current_sequence'] += 1
        else:
            user_answer, created = AnswerTraining.objects.get_or_create(
                user=request.user,
                defaults={
                    'correct_sequence': request.session['current_sequence'],
                    'is_correct': is_correct  # Установка значения is_correct
                }
            )

            if request.session['current_sequence'] > user_answer.correct_sequence:
                user_answer.correct_sequence = request.session['current_sequence']
                user_answer.save()

            request.session['current_sequence'] = 0
            return HttpResponseRedirect(reverse('resultinfotraining'))

    # Выбор случайного вопроса и перемешивание ответов
    questions = list(QuestionTraining.objects.all())
    random_question = random.choice(questions) if questions else None
    answers = []

    if random_question:
        answers = [random_question.answer_1, random_question.answer_2, random_question.answer_3, random_question.answer_4]
        random.shuffle(answers)

    return render(request, 'gametraining.html', {'question': random_question, 'answers': answers})

def result_info_training(request):
    # Получаем последний ответ пользователя
    last_answer = AnswerTraining.objects.filter(user=request.user).order_by('-id').first()
    correct_sequence = last_answer.correct_sequence if last_answer else 0

    return render(request, 'resultinfotraining.html', {'correct_answers_training': correct_sequence})

#Курс молодого бойца игра

@login_required(login_url='login')
def game_kmb(request):
    question = KmbQuestionStorage.objects.filter(
        id__gt=request.user.profile.last_question_id_kmb).first()  # Используем last_question_id_kmb здесь

    if question is None:
        answers = KmbAnswerStorage.objects.filter(
            user=request.user, right_answer=F('answer')).count()
        return redirect('resultinfo_kmb')

    if request.method == "POST":
        selected_answer = request.POST.get('answer')
        question_id = request.POST.get('question_id')
        question = get_object_or_404(KmbQuestionStorage, pk=question_id)

        existing_answer = KmbAnswerStorage.objects.filter(
            user=request.user, question=question).first()

        if existing_answer:
            existing_answer.answer = selected_answer
            existing_answer.save()
        else:
            KmbAnswerStorage.objects.create(
                user=request.user,
                question=question,
                answer=selected_answer,
                right_answer=question.correct_answer
            )

        request.user.profile.last_question_id_kmb = question.id  # Обновляем last_question_id_kmb
        request.user.profile.save()
        return redirect('kmb')

    answers = [question.answer1, question.answer2, question.answer3, question.answer4]
    random.shuffle(answers)
    return render(request, 'kmb.html', {'question': question, 'answers': answers})

@login_required(login_url='login')
def resultinfo_kmb(request):
    correct_answers = KmbAnswerStorage.objects.filter(
        user=request.user, right_answer=F('answer')).count()

    total_questions = KmbQuestionStorage.objects.count()
    return render(request, 'resultinfokmb.html', {'correct_answers': correct_answers, 'total_questions': total_questions})

@login_required(login_url='login')
def user_results_kmb(request):
    if not UserResultsKmbAccess.objects.first().is_access_enabled:
        return redirect('/kmb')  # Аналогичное перенаправление

    user_answers = KmbAnswerStorage.objects.filter(user=request.user)
    return render(request, 'user_results_kmb.html', {'user_answers': user_answers})