from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^contrats_json/$', 'jobs.views.contrat_json'),
    url(r'^contrats_exploit/$', TemplateView.as_view(template_name="jobs/contrats_exploit_json.html")),

    url(r'^admin/', include(admin.site.urls)),
)
