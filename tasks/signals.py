from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    if created:  # Si el usuario acaba de ser creado
        user_group, _ = Group.objects.get_or_create(name='Usuario')  # Asegúrate de que el grupo existe
        instance.groups.add(user_group)  # Asigna el grupo al usuario

from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in
from django.utils.timezone import now
from django.dispatch import receiver

@receiver(user_logged_in)
def logout_previous_sessions(sender, request, user, **kwargs):
    # Obtiene todas las sesiones activas
    sessions = Session.objects.filter(expire_date__gte=now())
    for session in sessions:
        data = session.get_decoded()
        # Si la sesión pertenece al usuario actual, la elimina
        if data.get('_auth_user_id') == str(user.id) and session.session_key != request.session.session_key:
            session.delete()