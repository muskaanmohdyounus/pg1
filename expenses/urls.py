from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),                    
    path('login/', views.login_view, name='login'),         
    path('logout/', views.logout_view, name='logout'),      

    path('expenses/', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('settings/', views.settings_page, name='settings'),
    path('edit/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),
    path('reports/', views.reports_page, name='reports'),
    path('signup/', views.signup, name='signup'),
    path("send-otp/", views.send_otp, name="send_otp"),
    path('onboarding/', views.onboarding_view, name='onboarding'),

]
