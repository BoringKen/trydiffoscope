import os
import celery
import shutil
import datetime
import traceback

from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.staticfiles.templatetags.staticfiles import static

from trydiffoscope.container.utils import call_in_container, kill_container

from .enums import StateEnum
from .models import Comparison
from .progress import set_progress

FOOTER = """
<div class="footer">
  <p style="float: left;">
    <a href="%(text_url)s">View text version</a>.
    Results are kept for {} days.
  </p>
  <p style="float: right; text-align: right; line-height: 24px;">
    Hosting provided by<br>
    <a href="https://www.bytemark.co.uk"><img src="%(bytemark_logo)s"></a>
  </p>
</div>
</body>
""".format(settings.TRYDIFFOSCOPE_RESULTS_RETENTION_DAYS)

@celery.task(soft_time_limit=90)
def execute_diffoscope(slug):
    comparison = Comparison.objects.get(slug=slug)

    cwd = os.path.abspath(default_storage.path(comparison.slug))

    # Mark as running
    comparison.state = StateEnum.running
    comparison.save(update_fields=('state',))

    p, tempdir = call_in_container((
        'diffoscope',
        '--status-fd=2',
        '--html', 'output.html',
        '--text', 'output.txt',
        '--profile=-',
        comparison.file_a.name.split(os.path.sep, 1)[1],
        comparison.file_b.name.split(os.path.sep, 1)[1],
    ), cwd)

    try:
        comparison.state = StateEnum.error

        for line in p.stderr:
            try:
                current, total = [int(x) for x in line.split('\t')[:2]]
                set_progress(comparison, current, total)
            except Exception:
                comparison.output += line

        comparison.output += p.communicate()[0]

        returncode = p.poll()
        html_output = os.path.join(cwd, 'output.html')

        if returncode == 0:
            comparison.state = StateEnum.identical
        elif returncode == 1:
            comparison.state = StateEnum.different

            try:
                with open(html_output, 'r') as f:
                    contents = f.read()

                with open(html_output, 'w') as f:
                    print >>f, contents.replace('</body>', FOOTER % {
                        'text_url': '%s.txt' % comparison.slug,
                        'bytemark_logo': static('images/bytemark.png'),
                    })
            except IOError:
                pass
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

        # Always delete uploaded files.
        for x in ('a', 'b'):
            shutil.rmtree(os.path.join(cwd, x), ignore_errors=True)

    return repr(comparison)
