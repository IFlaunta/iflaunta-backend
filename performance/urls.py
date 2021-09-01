from django.urls import path
from performance import views

app_name = 'performance'
urlpatterns = [
    path('add_user/', views.addUser.as_view(), name='add_user'),
    path('get_user_from_email/<email>/', views.getUserFromEmail.as_view(), name='get_user_from_email'),
    path('get_user_from_user_id/<int:user_id>/', views.getUserFromUserId.as_view(), name='get_user_from_user_id'),

    path('question/<int:question_id>/', views.question.as_view(), name='question'),
    path('question_list/', views.questionList.as_view(), name='question_list'),

]