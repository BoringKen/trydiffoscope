import os
import shutil
import tempfile
import subprocess

from django.conf import settings

from . import app_settings

def call_in_container(args, cwd):
    tempdir = tempfile.mkdtemp(prefix='trydiffoscope-')

    args = [
        'docker',
        'run',
        '--rm=true',
        '--net=none',
        '--user', app_settings.DOCKER_USER,
        '--read-only=true',
        '--memory', app_settings.DOCKER_MEMORY_LIMIT,
        '--cidfile', os.path.join(tempdir, 'cidfile'),
        '--workdir', cwd,
        '--volume', '%s:%s' % (cwd, cwd),
    ] + [
        '--cap-drop=%s' % x for x in app_settings.DOCKER_DROP_CAPABILITIES
    ] + [
        app_settings.DOCKER_IMAGE,
    ] + list(args)

    p = subprocess.Popen(
        args,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    return p, tempdir

def kill_container(tempdir):
    try:
        with open(os.path.join(tempdir, 'cidfile')) as f:
            container_id = f.read()
    except IOError:
        pass
    else:
        subprocess.call((
            'docker',
            'rm',
            '--force',
            container_id,
        ), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    shutil.rmtree(tempdir, ignore_errors=True)

def build_container(force=False):
    exists = bool(subprocess.check_output(
        ('docker', 'images', '-q', app_settings.DOCKER_IMAGE),
    ))

    if exists and not force:
        return

    subprocess.check_call((
        'docker',
        'build',
        '--no-cache',
        '--tag', app_settings.DOCKER_IMAGE,
        os.path.join(settings.STATIC_ROOT, 'docker'),
    ))

def clean_images():
    subprocess.call((
        'docker ps --all --quiet | xargs -r -L 1 docker rm',
    ), shell=True)

def clean_containers():
    subprocess.call((
        'docker images --filter dangling=true --quiet | xargs -r -L 1 docker rmi',
    ), shell=True)
