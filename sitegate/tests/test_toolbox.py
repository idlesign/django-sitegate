try:
    from django.urls import URLPattern

except ImportError:  # Django < 2.0
    from django.core.urlresolvers import RegexURLPattern as URLPattern


from sitegate.toolbox import get_sitegate_urls


def test_get_sitegate_urls():
    urls = get_sitegate_urls()
    assert isinstance(urls, list)
    assert len(urls) == 1
    assert isinstance(urls[0], URLPattern)
