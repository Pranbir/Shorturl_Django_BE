from django.urls import path

from . import views

urlpatterns = [
    path('report', views.report, name='report'),
    path('get_code', views.code_generator, name='code_gen'),
    path('<code>', views.code_handler, name='index'),
    path('', views.index, name='index'),
]