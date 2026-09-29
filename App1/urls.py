from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
     path("privacy/",views.PrivacyPolicy,name="privacy_policy"),
     path('create/',views.Complain_create,name='create_complaint'),
     path('login/',views.login_view,name="login"),
     path('logout/',views.logout_view,name="logout"),
     path('profile/',views.profile_view,name="profile"),
     path('detail/<int:complaint_id>/',views.Details,name="c_detail"),
    path("edit/<int:complaint_id>/", views.edit_View, name="edit_complaint"),
    path("delete/<int:complaint_id>/", views.delete_View, name="delete_complaint"),
    path("progress/",views.P_progress,name="Progress"),
    path("download-pdf/<int:complaint_id>/",views.download_complaint_pdf,name="download-pdf"),
    path("complaint-summary/",views.C_summery,name="complaint-summary"),
    path("change_passwrd/",views.change_password,name="change_password"),

    path(
    'forgot-password/',
    auth_views.PasswordResetView.as_view(
        template_name='forgot_password.html'
    ),
    name='password_reset'
),

path(
    'forgot-password/done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ),
    name='password_reset_done'
),

path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ),
    name='password_reset_confirm'
),

path(
    'reset/done/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ),
    name='password_reset_complete'
),
]
