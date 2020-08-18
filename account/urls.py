from django.urls import path

from account.views import LoginView, SignupView, VerificationView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name="signup"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
]
