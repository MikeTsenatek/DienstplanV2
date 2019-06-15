from django.urls import path

from . import views

app_name = 'dienste'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:dienstplanid>', views.IndexView.as_view(), name='bydienstplanid'),
    path('<int:dienstplanid>/<int:ordnerid>', views.IndexView.as_view(), name='byordnerid'),
    path('api/user/start/<int:funktionid>/<str:name>', views.userbyfunktion, name='apiuserprefix'),

]