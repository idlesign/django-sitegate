from django.urls import URLPattern

from sitegate.toolbox import get_sitegate_urls


def test_get_sitegate_urls():
    urls = get_sitegate_urls()
    assert isinstance(urls, list)
    assert len(urls) == 3
    assert isinstance(urls[0], URLPattern)
