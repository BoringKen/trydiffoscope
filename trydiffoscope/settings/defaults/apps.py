INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djcelery',
    'template_tests',

    'trydiffoscope.api',
    'trydiffoscope.container',
    'trydiffoscope.compare',
    'trydiffoscope.compare.retention_policy',
    'trydiffoscope.static',
    'trydiffoscope.utils',
)
