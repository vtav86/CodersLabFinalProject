"""CLFinalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from gym_app.views import LoginView, HomePageView, RegisterNewMemberView, OnlineRegistrationView, ManagePaymentView, \
    MyProfileView, ChangePasswordView, EditMyProfileView, LogoutView, ViewMembersView, MemberPaymentView, \
    EditMemberProfileView, ChangeMembershipNumberView, RegisterMemberVisitView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name="home"),
    # path('base/',BaseView.as_view(), name="baseview"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register-member/', RegisterNewMemberView.as_view(), name="registermember"),
    path('online-registration/', OnlineRegistrationView.as_view(), name="onlineregistration"),
    path('manage-payment/', ManagePaymentView.as_view(), name="managepayment"),
    path('my-profile/', MyProfileView.as_view(), name="myprofile"),
    path('change-password/', ChangePasswordView.as_view(), name="changepassword"),
    path('edit-my-profile/', EditMyProfileView.as_view(), name="editmyprofile"),
    path('view-members/', ViewMembersView.as_view(), name="viewmembers"),
    path('member-payment/<int:id>/', MemberPaymentView.as_view(), name="memberpayment"),
    path('edit-member-profile/<int:id>', EditMemberProfileView.as_view(), name="editmemberprofile"),
    path('change-membership-number/', ChangeMembershipNumberView.as_view(), name="changemembershipnumber"),
    path('register-member-visit/', RegisterMemberVisitView.as_view(), name="registermembervisit"),
]
