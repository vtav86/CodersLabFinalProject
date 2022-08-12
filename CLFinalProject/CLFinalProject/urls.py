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
    EditMemberProfileView, ChangeMembershipNumberView, RegisterMemberVisitView, CreateEventView, ViewAllEventsView, \
    ViewEventInfoView, MyEventsView, RegisterForEventView, AccessDeniedView, AboutUsView, PricingView, ContactUsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name="home"),
    path('about/', AboutUsView.as_view(), name="aboutus"),
    path('pricing/', PricingView.as_view(), name="pricing"),
    path('contact/', ContactUsView.as_view(), name="contactus"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register-member/', RegisterNewMemberView.as_view(), name="registermember"),
    path('online-registration/', OnlineRegistrationView.as_view(), name="onlineregistration"),
    path('manage-payment/', ManagePaymentView.as_view(), name="managepayment"),
    path('my-profile/', MyProfileView.as_view(), name="myprofile"),
    path('change-password/', ChangePasswordView.as_view(), name="changepassword"),  # addlink
    path('edit-my-profile/', EditMyProfileView.as_view(), name="editmyprofile"),  # addlink
    path('view-members/', ViewMembersView.as_view(), name="viewmembers"),
    path('member-payment/<int:id>/', MemberPaymentView.as_view(), name="memberpayment"),  # addlink
    path('edit-member-profile/<int:id>/', EditMemberProfileView.as_view(), name="editmemberprofile"),  # addlink
    path('change-membership-number/', ChangeMembershipNumberView.as_view(), name="changemembershipnumber"),
    path('register-member-visit/', RegisterMemberVisitView.as_view(), name="registermembervisit"),
    path('create-event/', CreateEventView.as_view(), name="createevent"),
    path('view-all-events/', ViewAllEventsView.as_view(), name="viewallevents"),
    path('view-event-info/<int:id>/', ViewEventInfoView.as_view(), name="vieweventinfo"),  # addlink
    path('my-events/', MyEventsView.as_view(), name="myevents"),  # checkaddlink
    path('view-event/<int:event_id>/', RegisterForEventView.as_view(), name="viewevent"),  # addlink
    path('access-denied', AccessDeniedView.as_view(), name="accessdenied"),


]
