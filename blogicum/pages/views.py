from django.views.generic import TemplateView
from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def internal_server_error(request):
    return render(request, 'pages/500.html', status=500)


class AboutBlogicum(TemplateView):
    ''' Возвращает HTML страницу '''
    template_name: str = 'pages/about.html'


class RulesBlogicum(TemplateView):
    ''' Возвращает HTML страницу '''
    template_name: str = 'pages/rules.html'
