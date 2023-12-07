from django.shortcuts import render, redirect
from .models import KmbButton, KmbSubmenu, KmbContent

def kmb_view(request):
    buttons = KmbButton.objects.all()
    return render(request, 'kmb.html', {'buttons': buttons})

def kmbsubmenu_view(request, button_id):
    submenus = KmbSubmenu.objects.filter(parent_button_id=button_id)
    return render(request, 'kmbsubmenu.html', {'submenus': submenus, 'button_id': button_id})

def content_view(request, submenu_id):
    contents = KmbContent.objects.filter(submenu_id=submenu_id)
    submenu = KmbSubmenu.objects.get(id=submenu_id)
    button_id = submenu.parent_button_id
    return render(request, 'content.html', {'contents': contents, 'button_id': button_id})


