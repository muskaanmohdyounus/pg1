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
    path('expenses/<int:id>/', views.expense_detail, name='expense_detail'),
    path('reports/', views.reports_page, name='reports'),
    path('signup/', views.signup, name='signup'),
    path("send-otp/", views.send_otp, name="send_otp"),
    path('onboarding/', views.onboarding_view, name='onboarding'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/add/', views.add_property, name='add_property'),
    path('properties/<int:id>/', views.property_detail, name='property_detail'),
    path('properties/<int:id>/edit/', views.edit_property, name='edit_property'),
    path('properties/<int:id>/delete/', views.delete_property, name='delete_property'),
    path('properties/graph/', views.property_graph, name='property_graph'),
    path("rent/add/", views.add_rent, name="add_rent"),
    path('tenant/rent/edit/<int:id>/', views.edit_rent, name='edit_rent'),
    path('tenant/rent/delete/<int:id>/', views.delete_rent, name='delete_rent'),
    path('tenant/rent/', views.tenant_rent, name='tenant_rent'),
    path('tenant/loans/', views.tenant_loan_list, name='tenant_loan_list'),
    path('tenant/loans/apply/', views.tenant_apply_loan, name='tenant_apply_loan'),
    path('tenant/loans/<int:pk>/edit/', views.tenant_edit_loan, name='tenant_edit_loan'),
    path('tenant/loans/<int:pk>/delete/', views.tenant_delete_loan, name='tenant_delete_loan'),
    path('login/select/', views.select_login_type, name='select_login_type'),
    path('tenant/login/', views.tenant_login, name='tenant_login'),
    path('tenant/signup/', views.tenant_signup, name='tenant_signup'),


]
