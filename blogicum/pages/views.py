from http import HTTPStatus

from django.shortcuts import render


def csrf_failure(request, reason=''):
    """Возвращает кастомную страницу 403."""
    return render(request, 'pages/403csrf.html',
                  status=HTTPStatus.FORBIDDEN)


def page_not_found(request, exception):
    """Возвращает кастомную страницу 404."""
    return render(request, 'pages/404.html',
                  status=HTTPStatus.NOT_FOUND)


def internal_server_error(request):
    """Возвращает кастомную страницу 500."""
    return render(request, 'pages/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR)
