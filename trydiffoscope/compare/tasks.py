import os
import celery
import datetime
import traceback

from django.core.files.storage import default_storage

from trydiffoscope.container.utils import call_in_container, kill_container

from .enums import StateEnum
from .models import Comparison

FOOTER = """
<div class="footer">
  <a href="%s.txt">View text version</a>
</div>
"""

@celery.task(soft_time_limit=60)
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

        returncode = p.poll()
        html_output = os.path.join(cwd, 'output.html')

        if returncode == 0:
            comparison.state = StateEnum.identical
        elif os.path.exists(html_output):
            try:
                with open(html_output, 'a') as f:
                    print >>f, FOOTER % comparison.slug
            except IOError:
                pass
        else:
            # If we didn't generate output.html, there was an error
            comparison.state = StateEnum.error
    except celery.exceptions.SoftTimeLimitExceeded:
        comparison.state = StateEnum.timeout
    except Exception:
        comparison.state = StateEnum.error
        comparison.output += '\n'
        comparison.output += traceback.format_exc()
    finally:
        comparison.updated = datetime.datetime.utcnow()
        comparison.save()
        kill_container(tempdir)

    return repr(comparison)
