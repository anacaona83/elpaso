from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="jobs/home.html")),
    url(r'^contrats/$', TemplateView.as_view(template_name="jobs/contrats_exploit_json2.html")),
    url(r'^about/$', TemplateView.as_view(template_name="jobs/about.html")),

    url(r'^contrats_json/$', 'jobs.views.contrat_json'),
    url(r'^contrats_camemberts/$', TemplateView.as_view(template_name="jobs/contrats_camemberts.html")),
    url(r'^stacks/$', TemplateView.as_view(template_name="jobs/contrats_stacks_nvd3.html")),

    url(r'^admin/', include(admin.site.urls)),
)
