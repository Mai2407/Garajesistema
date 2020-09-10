from django.urls import path

from . import views


urlpatterns = [

    path('', views.inicio),
    path('user_view/', views.user_view),
    path('index/', views.index, name='index'),
    path('registrados/', views.registrados, name='registrados'),
    path('registrar/', views.registrar, name='registrar'),
    path('no_activo/', views.no_activo, name='no_activo'),
    path('date_in/', views.date_in, name='date_in'),
    path('<id>/delete', views.delete, name="delete"),
    path('<id>/update', views.update, name="update"),
    path('<id>/activo_or_not', views.activo_or_not, name="activo_or_not"),
    path('buscar/', views.Looking_For_Person),

]