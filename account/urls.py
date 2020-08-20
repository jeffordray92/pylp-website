from django.urls import path
from account.views import (
    LoginView,
    PhotoSignatureView,
    ProfileView,
    SignupView,
    VerificationView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name="signup"),
    path('signup/photo-signature/<pk>',
         PhotoSignatureView.as_view(), name="photo-sig"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('profile/', ProfileView.as_view(), name="profile")

]
