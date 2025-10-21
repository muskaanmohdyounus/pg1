from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),                    
    path('login/', views.login_view, name='login'),         
    path('logout/', views.logout_view, name='logout'),      

    path('expenses/', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),
]
