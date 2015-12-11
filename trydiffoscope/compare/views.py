from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.static import serve
from django.core.files.storage import default_storage
from django.views.decorators.cache import never_cache

from .forms import CompareForm
from .enums import StateEnum
from .models import Comparison

def view(request):
    if request.method == 'POST':
        form = CompareForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save()

            return redirect('compare:poll', instance.slug)
    else:
        form = CompareForm()

    return render(request, 'compare/view.html', {
        'form': form,
    })

@never_cache
def poll(request, slug):
    comparison = get_object_or_404(Comparison, slug=slug)

    state = comparison.get_state_enum()

    if state == StateEnum.different:
        return redirect('compare:output', comparison.slug, 'html')

    return render(request, 'compare/states/%s.html' % state.name, {
        'comparison': comparison,
    })

def output(request, slug, extension):
    assert settings.DEBUG, "Overridden by nginx configuration"

    return serve(
        request,
        'output.%s' % extension,
        document_root=default_storage.path(slug),
    )
