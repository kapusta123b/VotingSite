from django.urls import path

from . import views


app_name = 'polls'

urlpatterns = [
    path('create/', views.CreatePollView.as_view(), name='create'),
    path('delete/<int:question_id>', views.DeletePollView.as_view(), name='delete'),
    path('<slug:category_slug>/', views.MainPollsView.as_view(), name='index'),
    path('<slug:category_slug>/<int:question_id>/', views.DetailPollView.as_view(), name='detail'),
    path('<slug:category_slug>/<int:question_id>/results/', views.PollResultView.as_view(), name='results'),
    path('<slug:category_slug>/<int:question_id>/vote/', views.vote, name='vote'),
]
