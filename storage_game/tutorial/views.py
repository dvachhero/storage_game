from django.shortcuts import render, redirect
from .models import KmbButton, KmbSubmenu, KmbContent
from django.core.paginator import Paginator

def kmb_view(request):
    buttons = KmbButton.objects.all()
    return render(request, 'kmb.html', {'buttons': buttons})

def kmbsubmenu_view(request, button_id):
    submenus = KmbSubmenu.objects.filter(parent_button_id=button_id)
    return render(request, 'kmbsubmenu.html', {'submenus': submenus, 'button_id': button_id})

def content_view(request, submenu_id):
    contents_list = KmbContent.objects.filter(submenu_id=submenu_id)
    paginator = Paginator(contents_list, 1)  # Показывать по 1 элементу на странице

    page_number = request.GET.get('page', 1)  # Получить номер страницы из запроса
    contents = paginator.get_page(page_number)

    submenu = KmbSubmenu.objects.get(id=submenu_id)
    button_id = submenu.parent_button_id

    return render(request, 'content.html', {
        'contents': contents,
        'button_id': button_id,
        'submenu_id': submenu_id
    })


