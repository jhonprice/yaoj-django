from django.conf.urls import url

from . import views


urlpatterns = [
    url('^$', views.index, name='index'),
    url('^faq', views.faq, name='faq'),
    url('^problem/index/$', views.problem_list, name='problem_list'),
    url('^problem/(?P<problem_id>[0-9]+)/$', views.problem_detail,
        name='problem_detail'),
    url('^problem/(?P<problem_id>[0-9]+)/status$', views.problem_status,
        name='problem_status'),
    url('^problem/(?P<problem_id>[0-9]+)/submit$', views.problem_submit,
        name='problem_submit'),
]
