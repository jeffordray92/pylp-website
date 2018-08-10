from content.models import SocialMedia, Header

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
