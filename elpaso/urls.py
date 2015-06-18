from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', TemplateView.as_view(template_name="jobs/home.html")),
    url(r'^$', 'jobs.views.stats_home'),
    url(r'^contrats/$', TemplateView.as_view(template_name="jobs/contrats.html")),
    url(r'^technos/$', TemplateView.as_view(template_name="jobs/technologies.html")),
    url(r'^semantique/$', TemplateView.as_view(template_name="jobs/semantique.html")),
    url(r'^contrats_json/$', 'jobs.views.contrat_json'),
    url(r'^contrats_camemberts/$', TemplateView.as_view(template_name="jobs/contrats_camemberts.html")),
    url(r'^stacks/$', TemplateView.as_view(template_name="jobs/contrats_stacks_nvd3.html")),
    url(r'^timeline/$', TemplateView.as_view(template_name="jobs/timeline.html")),
    url(r'^contrats_bis/$', TemplateView.as_view(template_name="jobs/contrats_exploit_json2.html")),

    url(r'^admin/', include(admin.site.urls)),
)
