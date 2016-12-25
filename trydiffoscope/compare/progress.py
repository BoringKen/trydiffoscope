from django.core.cache import cache

CACHE_KEY = 'progress:%s'

def get_progress(comparison):
    return cache.get(CACHE_KEY % comparison.slug) or (0, 1)

def set_progress(comparison, current, total):
    cache.set(CACHE_KEY % comparison.slug, (current, total))
