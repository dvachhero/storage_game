from django.shortcuts import render
from .models import AssistantButton
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def chat_page(request):
    buttons = AssistantButton.objects.all().prefetch_related('submenus')
    return render(request, 'chat_page.html', {'buttons': buttons})