from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/login/', views.login, name='login'),
    path('api/logout/', views.logout, name='logout'),
    path('api/user/', views.user, name='user'),
    path('api/guardies/<int:id_absencia>/', views.guards_by_id, name="Guàrdies per l'absència"),
    path('api/guardies/<slug:slug>/', views.guards_by_date, name="Guardies del dia"),
    path('api/guardies/', views.guards, name='Guàrdies'),
    path('api/absencies/<int:id_absencia>/', views.deleteAbsencia, name='deleteAbsencia'),
    path('api/absencies/', views.Absencies, name='Absencies'),
    path('api/grups/', views.updateGrups, name='updateGrups'),
    path('api/espais/', views.updateEspais, name='updateEspais'),
    path('api/materies/', views.updateMateries, name='updateMateries'),
    path('api/horari/<int:id_horari>/', views.updateHorari, name='updateHorari'),
    path('edit', views.edit, name='edit')
]