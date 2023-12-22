from django.contrib import admin
from django.urls import path
from game.views import home, logout_view, play, result, rules, game, resultinfo, user_results, game_menu, game_training, result_info_training, game_kmb, resultinfo_kmb, user_results_kmb
from bot.views import chat_page
from tutorial.views import kmb_view, kmbsubmenu_view, content_view
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('storage_game/admin/', admin.site.urls),
    path('storage_game/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('storage_game/home/', home, name='home'),  # Здесь login_required уже применено в views.py
    path('storage_game/play/', play, name='game'),
    path('storage_game/results/', result, name='result'),  # Используйте result вместо results
    path('storage_game/rules/', rules, name='rules'),
    path('storage_game/logout/', logout_view, name='logout'),
    path('storage_game/game/', game, name='game'),
    path('storage_game/resultinfo/', resultinfo, name='resultinfo'),
    path('storage_game/user_results/', user_results, name='user_results'),
    path('storage_game/chat/', chat_page, name='chat_page'),
    path('storage_game/', home, name='home'),
    path('storage_game/kmb/', kmb_view, name='kmb'),
    path('storage_game/kmbsubmenu/<int:button_id>/', kmbsubmenu_view, name='kmbsubmenu'),
    path('storage_game/content/<int:submenu_id>/', content_view, name='content'),
    path('storage_game/gamemenu/', game_menu, name='gamemenu'),
    path('storage_game/gametraining/', game_training, name='gametraining'),
    path('storage_game/resultinfotraining/', result_info_training, name='resultinfotraining'),
    path('storage_game/gamekmb/', game_kmb, name='game_kmb'),
    path('storage_game/resultinfokmb/', resultinfo_kmb, name='resultinfo_kmb'),
    path('storage_game/user_results_kmb/', user_results_kmb, name='user_results_kmb')
]
