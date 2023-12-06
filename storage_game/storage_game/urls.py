from django.contrib import admin
from django.urls import path
from game.views import login_view, home, logout_view, play, result, rules, game, resultinfo, user_results
from bot.views import chat_page
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('/login/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),  # Здесь login_required уже применено в views.py
    path('play/', play, name='game'),
    path('results/', result, name='result'),  # Используйте result вместо results
    path('rules/', rules, name='rules'),
    path('logout/', logout_view, name='logout'),
    path('game/', game, name='game'),
    path('resultinfo/', resultinfo, name='resultinfo'),
    path('user_results/', user_results, name='user_results'),
    path('chat/', chat_page, name='chat_page'),
    path('', redirect_to_login),
]
