from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from gdstorage.storage import GoogleDriveStorage
from content.models import ContactUsEmail
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

EDUCATIONAL_TYPE = (
    ('E', 'Elementary'),
    ('H', 'High School'),
    ('C', 'College'),
    ('P', 'Post Graduate'),
)


def year_choices():
    return [(r, r) for r in range(2004, datetime.now().date().year+1)]


def current_year():
    return datetime.now().date().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def send_email(photo=None, e_sig=None):
    subject = ""
    body = ""
    contact_email = ""
    try:
        contact_email = ContactUsEmail.objects.first().email
    except:
        contact_email = ""
    if photo and e_sig:
        subject = "[Photo & E-Signature Update]"
        body = f"Updated Photo: {photo} \n\n Updated E-Signature: {e_sig}"
    elif photo:
        subject = "[Photo Update]"
        body = f"Updated Photo: {photo}"
    elif e_sig:
        subject = "[E-Signature Update]"
        body = f"Updated E-Signature: {e_sig}"

    email = EmailMessage(
        subject,
        body,
        'noreply@pylp.com',
        [contact_email],
    )
    email.send(fail_silently=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    cluster = models.ForeignKey(
        "Cluster", on_delete=models.CASCADE, null=True, blank=True)
    committees = models.ManyToManyField('Committee', blank=True)
    is_verified = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='photos', blank=True,
                              null=True, verbose_name=u"Profile Picture")
    electronic_signature = models.ImageField(upload_to='e_signature', blank=True,
                                             null=True, verbose_name=u"Electronic Signature")
    email = models.EmailField(null=True)
    first_name = models.CharField(
        max_length=100, null=True, verbose_name=u"First Name")
    last_name = models.CharField(
        max_length=100, null=True, verbose_name=u"Last Name")
    birth_date = models.DateField(null=True, verbose_name=u"Date of Birth")
    birth_place = models.CharField(
        max_length=100, null=True, verbose_name=u"Place of Birth")
    civil_status = models.CharField(
        max_length=100, null=True, verbose_name=u"Civil Status")
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default="M")
    pylp_batch = models.PositiveIntegerField(
        null=True, verbose_name=u"PYLP Batch")
    pylp_year = models.IntegerField(
        null=True, validators=[MinValueValidator(1984), max_value_current_year], verbose_name=u"PYLP Year")
    host_family = models.CharField(
        max_length=100, null=True, verbose_name=u"Host Family")
    present_address = models.CharField(
        max_length=150, null=True, verbose_name=u"Present Address")
    permanent_address = models.CharField(
        max_length=150, null=True, verbose_name=u"Permanent Address")
    current_work_affiliation = models.CharField(
        max_length=100, null=True, verbose_name=u"Current Work Affiliation")
    name_address_office_school = models.CharField(
        max_length=150, null=True, verbose_name=u"Name and Address of Office")
    ethnicity = models.CharField(max_length=80, null=True)
    religion = models.CharField(max_length=80, null=True)
    facebook_account = models.CharField(
        max_length=80, null=True, verbose_name=u"Facebook Account")
    contact_number = PhoneNumberField(
        null=True, verbose_name=u"Contact Number", region="PH")
    telephone_number = PhoneNumberField(
        null=True, verbose_name=u"Telephone Number", region="PH")

    __original_photo = None
    __original_electronic_signature = None

    def __str__(self):
        return self.user.username

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self.__original_photo = self.photo
        self.__original_electronic_signature = self.electronic_signature

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.photo != self.__original_photo and self.electronic_signature != self.__original_electronic_signature:
            photo = ""
            if not self.photo:
                photo = "User removed photo"
            else:
                photo = self.photo.url
            e_sig = ""
            if not self.electronic_signature:
                e_sig = "User removed E-Signature"
            else:
                e_sig = self.electronic_signature.url
            send_email(photo=photo, e_sig=e_sig)
        elif self.photo != self.__original_photo:
            photo = ""
            if not self.photo:
                photo = "User removed photo"
            else:
                photo = self.photo.url
            send_email(photo=photo)
        elif self.electronic_signature != self.__original_electronic_signature:
            e_sig = ""
            if not self.electronic_signature:
                e_sig = "User removed E-Signature"
            else:
                e_sig = self.electronic_signature.url
            send_email(e_sig=e_sig)

        super(Profile, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_photo = self.photo
        self.__original_electronic_signature = self.electronic_signature
        self.user.is_active = self.is_verified
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.email = self.email
        self.user.save()
        super(Profile, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.user.is_active = self.is_verified
        self.user.save()
        super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Profiles"


class EducationalBackground(models.Model):
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, editable=False, null=True)
    education_type = models.CharField(
        max_length=1, choices=EDUCATIONAL_TYPE, default="C")
    school = models.ForeignKey(
        "School", on_delete=models.CASCADE, null=True)
    inclusive_date = models.DateField(null=True)
    level_attained = models.CharField(max_length=150, null=True)

    class Meta:
        verbose_name_plural = "Educational Background"


class MembershipOrganization(models.Model):
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, editable=False, null=True)
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, null=True)
    inclusive_date = models.DateField(null=True)
    position_held = models.CharField(max_length=150, null=True)

    class Meta:
        verbose_name_plural = "Membership in Youth Organizations"


class CommunityActivity(models.Model):
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, editable=False, null=True)
    activity_name = models.CharField(max_length=150, null=True)
    activity_description = models.CharField(max_length=150, null=True)
    sponsor_organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, null=True)
    inclusive_date = models.DateField(null=True)

    class Meta:
        verbose_name_plural = "Involvement in Youth/Community Related Activities"


class School(models.Model):
    school_name = models.CharField(max_length=150, null=True)
    school_address = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.school_name


class Organization(models.Model):
    organization_name = models.CharField(max_length=150, null=True)
    organization_address = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.organization_name


class Cluster(models.Model):
    name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name


class Committee(models.Model):
    name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name
