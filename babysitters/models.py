from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)  # Unicité de l'email pour le parent
    phone = models.CharField(max_length=15)
    address = models.TextField()
    number_of_children = models.IntegerField()  # Nombre d'enfants
    children_ages = models.TextField()  # Âges des enfants
    description = models.TextField()  # Description des besoins

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Babysitter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)  # Unicité de l'email pour le babysitter
    phone = models.CharField(max_length=15)
    address = models.TextField()  # Adresse complète
    city = models.CharField(max_length=100, default='Unknown')
    latitude = models.FloatField(null=True, blank=True)  # Latitude pour géolocalisation
    longitude = models.FloatField(null=True, blank=True)  # Longitude pour géolocalisation
    experience_years = models.IntegerField()
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2)
    bio = models.TextField()  # Description personnelle
    certifications = models.FileField(upload_to='certifications/', blank=True, null=True)  # Certificats (optionnel)
    languages_spoken = models.CharField(max_length=255, blank=True, null=True)  # Langues parlées
    availability = models.JSONField(null=True, blank=True)  # Jours/horaires de disponibilité
    photo = models.ImageField(upload_to='static/babysitter_photos/', blank=True, null=True, default='static/babysitter_photos/avatar.jpg')
    location = models.CharField(max_length=255, blank=True, null=True)  # Adresse ou localisation du babysitter
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def is_available(self, day, time_range):
        """
        Méthode pour vérifier si le babysitter est disponible
        :param day: Jour (ex: 'monday', 'tuesday', etc.)
        :param time_range: Tuple (heure début, heure fin), exemple : ('08:00', '12:00')
        :return: True si disponible, False sinon
        """
        if not self.availability:
            return False
        day_availability = self.availability.get(day, [])
        for available_range in day_availability:
            if time_range[0] >= available_range[0] and time_range[1] <= available_range[1]:
                return True
        return False

class Reservation(models.Model):
    parent = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    babysitter = models.ForeignKey(Babysitter, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'En attente'), ('confirmed', 'Confirmée'), ('cancelled', 'Annulée')], default='pending')

    def __str__(self):
        return f"Reservation from {self.parent} with {self.babysitter} on {self.date} at {self.start_time}"

    @staticmethod
    def has_reservation(parent, babysitter):
        """Check if a parent has a reservation with the babysitter."""
        return Reservation.objects.filter(parent=parent, babysitter=babysitter, status__in=['pending', 'confirmed']).exists()

