from jinja2 import Environment
from django.templatetags.static import static as staticfiles_storage
from django.urls import reverse

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage,
        'url': reverse,
    })
    return env