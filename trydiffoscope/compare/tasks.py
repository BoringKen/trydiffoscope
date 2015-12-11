import os
import celery
import datetime

from django.core.files.storage import default_storage

from trydiffoscope.container.utils import call_in_container, kill_container

from .enums import StateEnum
from .models import Comparison

@celery.task(soft_time_limit=15)
def execute_diffoscope(slug):
    comparison = Comparison.objects.get(slug=slug)

    cwd = os.path.abspath(default_storage.path(comparison.slug))

    # Mark as running
    comparison.state = StateEnum.running
    comparison.save(update_fields=('state',))

    p, tempdir = call_in_container((
        'diffoscope',
        '--debug',
        '--html', 'output.html',
        '--text', 'output.txt',
        comparison.file_a.name.split(os.path.sep, 1)[1],
        comparison.file_b.name.split(os.path.sep, 1)[1],
    ), cwd)

    try:
        comparison.state = StateEnum.different
        comparison.output = p.communicate()[0]

        if p.poll() == 0:
            comparison.state = StateEnum.identical
        elif not os.path.exists(os.path.join(cwd, 'output.html')):
            comparison.state = StateEnum.error
    except celery.exceptions.SoftTimeLimitExceeded, exc:
        comparison.state = StateEnum.timeout
    except Exception, exc:
        comparison.state = StateEnum.error
        comparison.output += repr(exc)
    finally:
        comparison.updated = datetime.datetime.utcnow()
        comparison.save()
        kill_container(tempdir)

    return repr(comparison)
