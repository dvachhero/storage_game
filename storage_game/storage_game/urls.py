from django.contrib import admin
from django.urls import path
from game.views import login_view, home, logout_view, play, result, rules, game, resultinfo, user_results, game_menu, game_training, result_info_training, game_kmb, resultinfo_kmb, user_results_kmb
from bot.views import chat_page
from tutorial.views import kmb_view, kmbsubmenu_view, content_view
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
    path('kmb/', kmb_view, name='kmb'),
    path('kmbsubmenu/<int:button_id>/', kmbsubmenu_view, name='kmbsubmenu'),
    path('content/<int:submenu_id>/', content_view, name='content'),
    path('gamemenu/', game_menu, name='gamemenu'),
    path('gametraining/', game_training, name='gametraining'),
    path('resultinfotraining/', result_info_training, name='resultinfotraining'),
    path('gamekmb/', game_kmb, name='game_kmb'),
    path('resultinfokmb/', resultinfo_kmb, name='resultinfo_kmb'),
    path('user_results_kmb/', user_results_kmb, name='user_results_kmb')

]
