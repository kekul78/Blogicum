from django.conf.urls.static import static
from django.views.generic.edit import CreateView
from django.contrib import admin

from users.forms import CustomUserCreationForm
from django.urls import include, path, reverse_lazy
from django.conf import settings


urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('blog:profile'),
        ),
        name='registration',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'pages.views.page_not_found'

handler500 = 'pages.views.internal_server_error'
