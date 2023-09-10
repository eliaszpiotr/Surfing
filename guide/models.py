from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
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


class Surfboard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    brand = models.CharField(max_length=64, blank=True, null=True)
    length = models.CharField(max_length=10, blank=True, null=True)
    width = models.CharField(max_length=10, blank=True, null=True)
    thickness = models.CharField(max_length=10, blank=True, null=True)
    volume = models.CharField(max_length=10, blank=True, null=True)

    class Construction(models.TextChoices):
        EPS_EPOXY = 'EPS/Epoxy', 'EPS/Epoxy'
        PU_POLYESTER = 'PU/Polyester', 'PU/Polyester'
        WOOD = 'Wood', 'Wood'
        OTHER = 'Other', 'Other'

    construction = models.CharField(max_length=64, choices=Construction.choices, blank=True, null=True)

    class FinSetup(models.TextChoices):
        SINGLE_FIN = 'Single fin', 'Single fin'
        TWIN_FIN = 'Twin fin', 'Twin fin'
        THRUSTER = 'Thruster', 'Thruster'
        QUAD = 'Quad', 'Quad'
        FIVE_FIN = 'Five fin', 'Five fin'
        OTHER = 'Other', 'Other'

    fin_setup = models.CharField(max_length=64, choices=FinSetup.choices, blank=True, null=True)

    class Tail(models.TextChoices):
        PIN = 'Pin', 'Pin'
        ROUND = 'Round', 'Round'
        SQUARE = 'Square', 'Square'
        SWALLOW = 'Swallow', 'Swallow'
        SQUASH = 'Squash', 'Squash'
        FISH = 'Fish', 'Fish'
        OTHER = 'Other', 'Other'

    tail = models.CharField(max_length=64, choices=Tail.choices, blank=True, null=True)

    class Nose(models.TextChoices):
        ROUND = 'Round', 'Round'
        POINTED = 'Pointed', 'Pointed'
        OTHER = 'Other', 'Other'

    nose = models.CharField(max_length=64, choices=Nose.choices, blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.name} {self.length}"


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
    # location = models.PointField(blank=False, null=False)
    country = CountryField(blank_label='(select country)', blank=False, null=False)
    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)

    class Continent(models.TextChoices):
        AFRICA = 'AF', 'Africa'
        ASIA = 'AS', 'Asia'
        EUROPE = 'EU', 'Europe'
        NORTH_AMERICA = 'NA', 'North America'
        SOUTH_AMERICA = 'SA', 'South America'
        AUSTRALIA = 'AU', 'Australia'
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

    # class Tide(models.TextChoices):
    #     H = 'H', 'High'
    #     L = 'L', 'Low'
    #
    # best_tide = models.CharField(max_length=1, choices=Tide.choices)

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

    danger = models.ManyToManyField(Danger, blank=True, )

    class Verification(models.TextChoices):
        VERIFIED = 'V', 'Verified'
        UNVERIFIED = 'U', 'Unverified'
        REJECTED = 'R', 'Rejected'

    verification = models.CharField(default='U', max_length=1)

    def __str__(self):
        return f'{self.name}, {self.continent}'

    def get_absolute_url(self):
        return reverse('spot', kwargs={'pk': self.pk})

    def verify(self):
        self.verification = 'V'
        self.save()

    def reject(self):
        self.verification = 'R'
        self.save()


class UserProfile(models.Model):
    # TODO: add users continent maybe?

    """
    Model for user profile
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    country = CountryField(blank_label='(select country)', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    home_spot = models.ForeignKey('SurfSpot', on_delete=models.SET_NULL, blank=True, null=True, )
    profile_picture = models.ImageField(upload_to='profile_pictures', default='profile_pictures/def.jpeg')
    visited_spots = models.ManyToManyField(SurfSpot, blank=True, related_name='visited_spots')
    friends = models.ManyToManyField(CustomUser, blank=True, related_name='friends')

    # boards = models.ManyToManyField(Surfboard, blank=True, related_name='boards')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.id)])

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)


class Comment(models.Model):
    """
    Model for comment on a spot
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    spot = models.ForeignKey(SurfSpot, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.spot.name}'

    def get_absolute_url(self):
        return reverse('spot', kwargs={'pk': self.spot.pk})


class Rating(models.Model):
    """
    Model for rating a spot
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    spot = models.ForeignKey(SurfSpot, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'{self.user.username} - {self.spot.name}'

    def get_absolute_url(self):
        return reverse('spot', kwargs={'pk': self.spot.pk})


class Photo(models.Model):
    """
    Model for photo of a spot
    """
    spot = models.ForeignKey(SurfSpot, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='spot_photos')
    date = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.spot.name} - {self.photo.name}'

    def get_absolute_url(self):
        return reverse('spot', kwargs={'pk': self.spot.pk})


class Report(models.Model):
    """
    Model for reporting a spot
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    spot = models.ForeignKey(SurfSpot, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.spot.name}'

    def get_absolute_url(self):
        return reverse('spot', kwargs={'pk': self.spot.pk})


class Message(models.Model):
    """
    Model for messaging a user
    """
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} - {self.receiver.username}'

    def get_absolute_url(self):
        return reverse('message', kwargs={'pk': self.pk})


class SurfingMeeting(models.Model):
    spot = models.ForeignKey(SurfSpot, on_delete=models.CASCADE)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organized_meetings")
    date_time = models.DateTimeField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="meetings_joined", blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Meeting at {self.spot.name} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"
