from django.urls import path

from . import views


app_name = 'polls'

urlpatterns = [
    path('create/', views.create_poll, name='create'),
    path('<slug:category_slug>/', views.MainPollsView.as_view(), name='index'),
    path('<slug:category_slug>/<int:question_id>/', views.DetailPollView.as_view(), name='detail'),
    path('<slug:category_slug>/<int:question_id>/results/', views.results, name='results'),
    path('<slug:category_slug>/<int:question_id>/vote/', views.vote, name='vote'),
]
