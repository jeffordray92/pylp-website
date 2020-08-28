from dal import autocomplete
from django.urls import path
from django.conf.urls import url
from account.views import (
    LoginView,
    PhotoSignatureView,
    ProfileView,
    SignupView,
    organization_autocomplete,
    school_autocomplete,
    VerificationView,
)
from account.models import School
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name="signup"),
    path('signup/photo-signature/<pk>',
         PhotoSignatureView.as_view(), name="photo-sig"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('profile/', ProfileView.as_view(), name="profile"),
    url(r'^school-autocomplete/$', school_autocomplete.as_view(create_field='school_name'),
        name='school-autocomplete'),
    url(r'^organization-autocomplete/$', organization_autocomplete.as_view(create_field='organization_name'),
        name='organization-autocomplete')

]
