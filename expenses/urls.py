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
    path('tenant/login/', views.tenant_login, name='tenant_login'),
    path('tenant/loans/', views.tenant_loan_list, name='tenant_loan_list'),
    path('tenant/loans/apply/', views.tenant_apply_loan, name='tenant_apply_loan'),
    path('tenant/loans/<int:pk>/edit/', views.tenant_edit_loan, name='tenant_edit_loan'),
    path('tenant/loans/<int:pk>/delete/', views.tenant_delete_loan, name='tenant_delete_loan'),
    path('login/select/', views.select_login_type, name='select_login_type'),
    path('tenant/signup/', views.tenant_signup, name='tenant_signup'),
    
    # OWNER LOAN URLS
    path("owner/loans/", views.owner_loan_list, name="owner_loan_list"),
    path("owner/loans/approve/", views.approve_loan, name="approve_loan"),
    path("owner/loans/<int:pk>/reject/", views.reject_loan, name="reject_loan"),
    path('owner/loans/<int:pk>/edit/', views.edit_approved_loan, name='edit_approved_loan'),
    # Delete approved loan
    path('owner/<int:pk>/delete/', views.delete_approved_loan, name='delete_approved_loan'),

    # OWNER TENANT MANAGEMENT & KYC
    path('tenants/', views.owner_tenant_list, name='owner_tenant_list'),
    path('tenants/add/', views.add_owner_tenant, name='add_owner_tenant'),
    path('tenants/edit/<int:id>/', views.edit_owner_tenant, name='edit_owner_tenant'),
    path('tenants/delete/<int:id>/', views.delete_owner_tenant, name='delete_owner_tenant'),
    path('tenant/<int:tenant_id>/kyc-review/', views.owner_review_kyc, name='owner_review_kyc'),
    path('tenant/<int:tenant_id>/kyc/approve/', views.approve_kyc, name='approve_kyc'),
    path('tenant/<int:tenant_id>/kyc/reject/', views.reject_kyc, name='reject_kyc'),
    path('tenant/<str:tenant_unique_id>/kyc/', views.tenant_kyc, name='tenant_kyc'),
    path('kyc/approvals/', views.kyc_approval_list, name='kyc_approval_list'),


        # ---------------------------
    # Owner Rental URLs
    # ---------------------------
    path('owner/rentals/', views.owner_rental_dashboard, name='owner_rental_dashboard'),
    path('owner/rentals/create/', views.owner_create_rent, name='owner_create_rent'),
    path('owner/rentals/edit/<int:rent_id>/', views.owner_edit_rent, name='owner_edit_rent'),
    path('owner/rentals/delete/<int:rent_id>/', views.owner_delete_rent, name='owner_delete_rent'),
    path('owner/rentals/mark-paid/<int:rent_id>/', views.owner_mark_rent_paid, name='owner_mark_rent_paid'),
    path('owner/rent/paid/<int:rent_id>/', views.owner_paid_rent_detail, name='owner_paid_rent_detail'),
    path('tenant/rentals/', views.tenant_rentals, name='tenant_rental_dashboard'),
    path('tenant/rentals/pay/<int:rent_id>/', views.tenant_pay_rent, name='tenant_pay_rent'),
    path('tenant/rentals/paid/<int:rent_id>/', views.tenant_paid_rent_details, name='tenant_paid_rent_details'),

]  
