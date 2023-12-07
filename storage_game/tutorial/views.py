from django.shortcuts import render
from .models import KmbButton, KmbSubmenu, KmbContent

def kmb_view(request):
    submenu_id = request.GET.get('submenu_id')
    content_id = request.GET.get('content_id')
    next_content = None
    current_submenu = None

    if submenu_id:
        current_submenu = KmbSubmenu.objects.filter(id=submenu_id).first()
        contents = KmbContent.objects.filter(submenu_id=submenu_id).order_by('id')

        if content_id:
            current_content = contents.filter(id=content_id).first()
            next_content = contents.filter(id__gt=content_id).first()
        else:
            current_content = contents.first()
            if current_content:
                next_content = contents.filter(id__gt=current_content.id).first()
    else:
        current_content = None

    # Получить все кнопки
    buttons = KmbButton.objects.all()

    if current_submenu and current_submenu.title == "kmbmenu":
        # Если текущее подменю - "kmbmenu", исключить кнопки "kmbmenu" из контекста
        buttons = buttons.exclude(title="kmbmenu")

    context = {
        'buttons': buttons,
        'current_submenu': current_submenu,
        'current_content': current_content,
        'next_content': next_content,
    }

    return render(request, 'kmb.html', context)
