from django.urls import path
from performance import views

app_name = 'performance'
urlpatterns = [
    path("add_user/", views.addUser.as_view(), name="add_user"),
    path("get_user_from_email/<email>/", views.getUserFromEmail.as_view(), name="get_user_from_email"),
    path("get_user_from_user_id/<int:user_id>/", views.getUserFromUserId.as_view(), name="get_user_from_user_id")

]