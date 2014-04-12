from django.conf.urls.defaults import patterns, include, url
from django.views.defaults import server_error, page_not_found
from django.utils.functional import curry

from settings import STATIC_ROOT, MEDIA_ROOT
from sites import site

handler500 = curry(server_error, template_name='admin/500.html')
handler404 = curry(page_not_found, template_name='admin/404.html')

urlpatterns = patterns('',
    url(r'^', include(site.urls)),                 
    
    # Static and media files
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
)
