from django.urls import path

from . import views

urlpatterns = [
    path('report', views.report, name='report'),
    path('report/<code>', views.report_code, name='report'),
    path('get_code', views.code_generator, name='code_gen'),
    path('search_code', views.search_code, name='search_code'),
    path('<code>', views.code_handler, name='index'),
    path('', views.index, name='index'),
]