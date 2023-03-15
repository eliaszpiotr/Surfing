from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.urls import reverse

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """
    Model for user profile
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=64, blank=True, null=True)
    country = CountryField(blank_label='(select country)', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    home_spot = models.ForeignKey('SurfSpot', on_delete=models.SET_NULL, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.id)])

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)


class Danger(models.Model):
    """
    Model for surf spot danger
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class SurfSpot(models.Model):
    """
    Model for surfing spot with location as a point on the map.
    """

    name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    description = models.TextField()
    country = CountryField(blank_label='(select country)', blank=False, null=False)
    # location = models.PointField(blank=False, null=False, extent=[-180, -90, 180, 90], tolerance=0.00001)

    class Continent(models.TextChoices):
        AFRICA = 'AF', 'Africa'
        ASIA = 'AS', 'Asia'
        EUROPE = 'EU', 'Europe'
        NORTH_AMERICA = 'NA', 'North America'
        SOUTH_AMERICA = 'SA', 'South America'
        OCEANIA = 'OC', 'Oceania'

    continent = models.CharField(choices=Continent.choices, max_length=2, blank=False, null=False)

    class Wind(models.TextChoices):
        NORTH = 'N', 'North'
        NORTH_EAST = 'NE', 'North-East'
        EAST = 'E', 'East'
        SOUTH_EAST = 'SE', 'South-East'
        SOUTH = 'S', 'South'
        SOUTH_WEST = 'SW', 'South-West'
        WEST = 'W', 'West'
        NORTH_WEST = 'NW', 'North-West'

    best_wind = models.CharField(max_length=13, choices=Wind.choices)

    class WaveDirection(models.TextChoices):
        L = 'L', 'Left'
        R = 'R', 'Right'
        B = 'B', 'Both'

    wave_direction = models.CharField(max_length=1, choices=WaveDirection.choices)

    class SpotType(models.TextChoices):
        B = 'B', 'Beach break'
        R = 'R', 'Reef break'
        P = 'P', 'Point break'
        O = 'O', 'Other'

    spot_type = models.CharField(max_length=1, choices=SpotType.choices)

    class WaveType(models.TextChoices):
        G = 'G', 'Gentle'
        M = 'M', 'Moderate'
        H = 'H', 'Heavy'
        E = 'E', 'Extreme'

    wave_type = models.CharField(max_length=1, choices=WaveType.choices)

    class WaveHeight(models.IntegerChoices):
        SMALL = 1, '1-3 ft.'
        MEDIUM = 2, '3-6 ft.'
        LARGE = 3, '6-9 ft.'
        HUGE = 4, '9-12 ft.'
        MASSIVE = 5, '12+ ft.'
        SUPERMASSIVE = 6, '20+ ft.'

    swell_size = models.IntegerField(choices=WaveHeight.choices)

    class Crowd(models.IntegerChoices):
        EMPTY = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4
        FULL = 5

    crowd = models.IntegerField(choices=Crowd.choices)

    class Difficulty(models.IntegerChoices):
        BEGINNER = 1
        INTERMEDIATE = 2
        ADVANCED = 3
        PRO = 4

    difficulty = models.IntegerField(choices=Difficulty.choices, blank=True, null=True)

    danger = models.ManyToManyField(Danger)

    def __str__(self):
        return f'{self.name}, {self.continent}'

    def get_absolute_url(self):
        return reverse('spot', kwargs={'pk': self.pk})
