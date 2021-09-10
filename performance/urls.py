from django.urls import path
from performance import views

app_name = 'performance'
urlpatterns = [
    path('add_user/', views.addUser.as_view(), name='add_user'),
    path('get_user/', views.getUser.as_view(), name="get_user"),
    path('public_user_from_email/<email>/', views.getUserPublicDataFromEmail.as_view(), name='get_public_user_from_email'),
    path('public_user_from_user_id/<int:user_id>/', views.getUserPublicDataFromUserId.as_view(), name='get_public_user_from_user_id'),

    path('question/<int:question_id>/', views.question.as_view(), name='question'),
    path('question_list/', views.questionList.as_view(), name='question_list'),

    path('logout/', views.userLogOut.as_view(), name="user_logout"),

    path('performance_list/', views.performanceList.as_view(), name="performance_list"),

]