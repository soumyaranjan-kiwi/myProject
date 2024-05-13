from django.urls import path
from . import views

urlpatterns = [
    path('fileupload/', views.showformdata, name='fileupload'),
    path('htmltable/', views.process_form_and_render_table, name='htmltable'),

]
