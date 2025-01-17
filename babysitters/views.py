from django.shortcuts import render,redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Parent, Babysitter ,Reservation,Notification
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, Page
from django.utils.timezone import now
from datetime import datetime
from django.utils import timezone
def register_choice(request):
    return render(request, 'register_choice.html')

def babysitter_register(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        experience_years = request.POST.get('experience_years')
        hourly_rate = request.POST.get('hourly_rate')
        bio = request.POST.get('bio')
        certifications = request.FILES.get('certifications')
        availability = request.POST.get('availability')
        password = request.POST.get('password')
        
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'register_babysitter.html')  # Ne pas rediriger, rester sur la même page

        # Vérification si l'email est déjà utilisé par un Parent
        if Parent.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé pour un compte Parent. Veuillez vous connecter avec ce compte.")
            return render(request, 'register_babysitter.html')

        # Vérification si l'email est déjà utilisé par un Babysitter
        if Babysitter.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé pour un compte Babysitter. Veuillez vous connecter avec ce compte.")
            return render(request, 'register_babysitter.html')

        # Récupérer ou créer un utilisateur avec l'email
        user, created = User.objects.get_or_create(email=email, username=email)
        if created:
            user.set_password(password)  # Attribuer le mot de passe
            user.save()

        # Créer un objet Babysitter
        babysitter = Babysitter(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            experience_years=experience_years,
            hourly_rate=hourly_rate,
            bio=bio,
            certifications=certifications,
            availability=availability
        )
        babysitter.save()

        # Message de succès
        messages.success(request, "Inscription réussie en tant que Babysitter. Vous pouvez maintenant vous connecter.")
        return redirect('login')

    return render(request, 'register_babysitter.html')

def register_parent(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        number_of_children = request.POST.get('number_of_children')
        children_ages = request.POST.get('children_ages')
        description = request.POST.get('description')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Vérification des mots de passe
        if password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'register_parent.html')  # Ne pas rediriger, rester sur la même page

        # Récupérer ou créer un utilisateur avec l'email
        user, created = User.objects.get_or_create(email=email, username=email,first_name=first_name,last_name=last_name)
        if created:
            user.set_password(password)  # Attribuer le mot de passe
            user.save()

        # Vérifier si l'email est déjà associé à un Babysitter
        if Babysitter.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé pour un compte Babysitter. Veuillez vous connecter avec ce compte.")
            return render(request, 'register_parent.html')  # Ne pas rediriger, rester sur la même page
        # Vérifier si l'email est déjà utilisé pour un compte Parent
        if Parent.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé pour un compte Parent. Veuillez vous connecter avec ce compte.")
            return render(request, 'register_parent.html')  # Ne pas rediriger, rester sur la même page

        # Créer un objet Parent
        parent = Parent(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            number_of_children=number_of_children,
            children_ages=children_ages,
            description=description
        )
        parent.save()

        # Rediriger vers la page de connexion
        messages.success(request, "Inscription réussie en tant que Parent. Vous pouvez maintenant vous connecter.")
        return redirect('login')

    return render(request, 'register_parent.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Chercher l'utilisateur par email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Email ou mot de passe incorrect.'})
        
        # Authentifier l'utilisateur
        user = authenticate(request, username=user.username, password=password)
        
        if user is not None:
            login(request, user)

            # Vérifie si l'utilisateur est un Parent ou un Babysitter
            try:
                # Si l'utilisateur est un Parent
                parent = Parent.objects.get(user=user)
                return redirect('parent_dashboard')  # Redirige vers le tableau de bord du parent
            except Parent.DoesNotExist:
                try:
                    # Si l'utilisateur est un Babysitter
                    babysitter = Babysitter.objects.get(user=user)
                    return redirect('babysitter_dashboard')  # Redirige vers le tableau de bord du babysitter
                except Babysitter.DoesNotExist:
                    return render(request, 'login.html', {'error': 'Ce compte n\'est ni un Parent ni un Babysitter.'})
        else:
            return render(request, 'login.html', {'error': 'Email ou mot de passe incorrect.'})
    
    return render(request, 'login.html')


@login_required
def parent_dashboard(request):
    try:
        parent = Parent.objects.get(user=request.user)  # Récupère l'objet Parent
    except Parent.DoesNotExist:
        parent = None

    # Calculer le nombre de notifications non lues pour le parent
    unread_notifications_count = Notification.objects.filter(user=request.user, read=False).count()

    # Passe l'objet Parent, l'utilisateur et le nombre de notifications non lues au template
    return render(request, 'parent_dashboard.html', {
        'user': request.user, 
        'parent': parent,
        'unread_notifications_count': unread_notifications_count
    })



@login_required
def babysitter_dashboard(request):
    try:
        babysitter = Babysitter.objects.get(user=request.user)  # Récupère l'objet Babysitter
    except Babysitter.DoesNotExist:
        babysitter = None

    

    # Passe l'objet Babysitter, l'utilisateur et le nombre de notifications non lues au template
    return render(request, 'babysitter_dashboard.html', {
        'user': request.user, 
        'babysitter': babysitter
    })

def home(request):
    return render(request, 'home.html')
def custom_logout(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('home')

def search_babysitters(request):
    # Récupérer les filtres de recherche
    availability_filter = request.GET.get('availability', '')
    location_filter = request.GET.get('location', '')
    
    babysitters = Babysitter.objects.all()
    
    # Appliquer les filtres de disponibilité et de localisation
    if availability_filter:
        babysitters = babysitters.filter(availability__icontains=availability_filter)
    
    if location_filter:
        babysitters = babysitters.filter(address__icontains=location_filter)
    
    # Préparer le statut des réservations pour les utilisateurs authentifiés
    reservation_status = {}
    parent_id = None  # Initialisation de parent_id

    if request.user.is_authenticated:
        try:
            parent = Parent.objects.get(user=request.user)  # Récupère l'instance Parent associée à l'utilisateur
            parent_id = parent.id  # Récupère l'ID du parent
        except Parent.DoesNotExist:
            # Si l'utilisateur connecté n'est pas un Parent, on ne fait rien ou on gère comme tu veux
            reservation_status = {}
    
    # Pagination
    paginator = Paginator(babysitters, 4)  # Affiche 4 babysitters par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Passer le contexte nécessaire à la vue
    return render(request, 'search_babysitters.html', {
        'babysitters': page_obj,
        'availability_filter': availability_filter,
        'location_filter': location_filter,
        'reservation_status': reservation_status,
        'parent_id': parent_id,  # Ajouter parent_id au contexte
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None
    })

def cancel_reservation(request, babysitter_id):
    babysitter = get_object_or_404(Babysitter, id=babysitter_id)

    # Trouver la réservation active et annuler
    reservation = Reservation.objects.filter(parent=request.user, babysitter=babysitter, status__in=['pending', 'confirmed']).first()
    if reservation:
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, f"Votre réservation avec {babysitter.first_name} a été annulée.")
    else:
        messages.error(request, "Aucune réservation active n'a été trouvée pour ce babysitter.")

    return redirect('search_babysitters')

def create_reservation_for(request, babysitter_id):
    babysitter = get_object_or_404(Babysitter, id=babysitter_id)

    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        duration = request.POST.get('duration')

        reservation_datetime_str = f"{date} {start_time}"
        reservation_datetime = datetime.strptime(reservation_datetime_str, "%Y-%m-%d %H:%M")
        reservation_datetime = timezone.make_aware(reservation_datetime)

        if reservation_datetime <= timezone.now():
            messages.error(request, "La date ou l'heure de réservation ne peut pas être dans le passé.")
            return redirect('create_reservation', babysitter_id=babysitter.id)

        # Vérifiez que l'utilisateur connecté est un Parent
        if request.user.is_authenticated:
            try:
                # Récupérer l'instance Parent associée à l'utilisateur connecté
                parent = Parent.objects.get(user=request.user)
            except Parent.DoesNotExist:
                messages.error(request, "Vous devez être un parent pour effectuer une réservation.")
                return redirect('search_babysitters')

            # Création de la réservation
            reservation = Reservation.objects.create(
                parent=parent,  # Utiliser l'instance Parent
                babysitter=babysitter,
                date=date,
                start_time=start_time,
                duration=duration,
            )
            reservation.save()

            # Création d'une notification pour le babysitter
            Notification.objects.create(
                user=babysitter.user,
                message=f"Vous avez une nouvelle réservation de {parent.user.username} ({parent.user.first_name} {parent.user.last_name}).",
                notification_type='reservation',
            )

            messages.success(request, f"Réservation créée avec succès pour {babysitter.first_name} {babysitter.last_name}.")
            return redirect('search_babysitters')

        else:
            messages.error(request, "Vous devez être connecté pour effectuer une réservation.")
            return redirect('login')  # Redirige l'utilisateur vers la page de connexion

    return render(request, 'create_reservation.html', {'babysitter': babysitter})

@login_required
def babysitter_profile(request):
    babysitter = get_object_or_404(Babysitter, user=request.user)
    return render(request, 'babysitter/babysitter_profile.html', {'babysitter': babysitter})

@login_required
def update_babysitter_profile(request):
    babysitter = get_object_or_404(Babysitter, user=request.user)
    if request.method == 'POST':
        babysitter.first_name = request.POST.get('first_name')
        babysitter.last_name = request.POST.get('last_name')
        babysitter.phone = request.POST.get('phone')
        babysitter.address = request.POST.get('address')
        babysitter.city = request.POST.get('city')
        babysitter.experience_years = request.POST.get('experience_years')
        babysitter.hourly_rate = request.POST.get('hourly_rate')
        babysitter.bio = request.POST.get('bio')
        babysitter.languages_spoken = request.POST.get('languages_spoken')
        babysitter.photo = request.FILES.get('photo') if request.FILES.get('photo') else babysitter.photo
        babysitter.save()
        return redirect('babysitter_dashboard')

    return render(request, 'update_babysitter_profile.html', {'babysitter': babysitter})

def babysitter_detail(request, babysitter_id):
    babysitter = get_object_or_404(Babysitter, id=babysitter_id)
    return render(request, 'babysitter_detail.html', {'babysitter': babysitter})

@login_required
def voir_reservations_babysitter(request, babysitter_id):
    # Vérifier si le babysitter correspond à l'utilisateur connecté
    babysitter = get_object_or_404(Babysitter, id=babysitter_id, user=request.user)

    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        action = request.POST.get('action')

        # Récupérer la réservation concernée
        reservation = get_object_or_404(Reservation, id=reservation_id, babysitter=babysitter)

        if action == 'accept':
            reservation.status = 'confirmed'
            reservation.save()

            # Créer une notification pour le parent
            Notification.objects.create(
                user=reservation.parent.user,  # Utilisateur lié au parent
                message=f"Votre réservation avec {babysitter.first_name} {babysitter.last_name} a été acceptée.",
                notification_type='reservation_accepted',
            )

        elif action == 'reject':
            reservation.status = 'cancelled'
            reservation.save()

            # Créer une notification pour le parent
            Notification.objects.create(
                user=reservation.parent.user,  # Utilisateur lié au parent
                message=f"Votre réservation avec {babysitter.first_name} {babysitter.last_name} a été rejetée.",
                notification_type='reservation_rejected',
            )

        return redirect('voir_reservations_babysitter', babysitter_id=babysitter.id)

    # Afficher toutes les réservations
    reservations = Reservation.objects.filter(babysitter=babysitter)
    return render(request, 'voir_reservations.html', {'reservations': reservations})

@login_required
def parent_reservations(request, parent_id):
    # Récupérer le parent en fonction de l'ID passé dans l'URL
    parent = get_object_or_404(Parent, id=parent_id)
    
    # Obtenir toutes les réservations du parent spécifié
    reservations = Reservation.objects.filter(parent=parent).order_by('-date', '-start_time')

    # Mettre à jour les réservations pour classer celles passées comme "passées"
    for reservation in reservations:
        try:
            # Créer un objet datetime à partir de la date et de l'heure de début de la réservation
            reservation_datetime_str = f"{reservation.date} {reservation.start_time}"
            reservation_datetime = datetime.strptime(reservation_datetime_str, "%Y-%m-%d %H:%M")

            # Vérifier si la réservation est dans le passé
            if reservation_datetime < datetime.now():
                if reservation.status != 'cancelled':
                    reservation.status = 'passed'  # Modifier le statut pour "passé"
                    reservation.save()

        except ValueError as e:
            print(f"Erreur de conversion de la date/heure : {e}")
            continue

    context = {
        'parent': parent,
        'reservations': reservations,
    }
    return render(request, 'parent_reservations.html', context)


@login_required
def update_parent_profile(request):
    # Récupérer l'objet Parent associé à l'utilisateur connecté
    parent = request.user.parent
    
    if request.method == 'POST':
        # Récupérer et mettre à jour les données du parent
        parent.first_name = request.POST.get('first_name')
        parent.last_name = request.POST.get('last_name')
        parent.email = request.POST.get('email')
        parent.phone = request.POST.get('phone')
        parent.address = request.POST.get('address')
        parent.number_of_children = request.POST.get('number_of_children')
        parent.children_ages = request.POST.get('children_ages')
        parent.description = request.POST.get('description')

        # Sauvegarder les modifications directement
        parent.save()

        # Message de succès après mise à jour
        messages.success(request, "Profil mis à jour avec succès !")
        return redirect('parent_dashboard')  # Rediriger vers la page après mise à jour

    return render(request, 'update_profile_parent.html', {'parent': parent})


@login_required
def notifications_parent(request):
    # Récupérer l'objet Parent
    try:
        parent = Parent.objects.get(user=request.user)
    except Parent.DoesNotExist:
        parent = None

    # Récupérer les notifications non lues du parent
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'parent': parent,
        'notifications': notifications,
    }
    return render(request, 'notifications_parent.html', context)




@login_required
def notifications_babysitter(request):
    # Récupérer les notifications non lues du babysitter connecté
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')  

    return render(request, 'notifications_babysitter.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = Notification.objects.filter(id=notification_id, user=request.user).first()

    if not notification:
        messages.error(request, "Notification introuvable ou non autorisée.")
        return redirect('notifications_parent' if hasattr(request.user, 'parent') else 'notifications_babysitter')

    notification.read = True
    notification.save()

    if hasattr(request.user, 'parent'):
        return redirect('notifications_parent')
    elif hasattr(request.user, 'babysitter'):
        return redirect('notifications_babysitter')

    return redirect('home')
    # Récupérer la notification par son ID
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)

    # Mettre la notification à jour comme lue
    notification.read = True
    notification.save()

    # Vérifier si l'utilisateur est un parent ou un babysitter
    if hasattr(request.user, 'parent'):  # Vérifie si l'utilisateur a un lien avec le modèle Parent
        return redirect('notifications_parent')
    elif hasattr(request.user, 'babysitter'):  # Vérifie si l'utilisateur a un lien avec le modèle Babysitter
        return redirect('notifications_babysitter')

    # Par défaut, rediriger vers la page d'accueil (au cas où l'utilisateur n'est ni parent ni babysitter)
    return redirect('home')