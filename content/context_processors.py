from content.models import SocialMedia, Header
from django.conf import settings


def social_media(request):
    socmed = SocialMedia.objects.first()
    return {'facebook': socmed.facebook,
            'twitter': socmed.twitter,
            'instagram': socmed.instagram,
            'linkedin': socmed.linkedin,
            'telephone': socmed.telephone,
            'email': socmed.email,
            'about': Header.objects.first().details
            }


def facebook_app_id(request):
    return {'facebook_app_id': settings.FACEBOOK_APP_ID}
