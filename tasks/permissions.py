from django.core.exceptions import PermissionDenied

def check_dynamic_permissions(user, recipe, action):
    """
    Verifica los permisos dinámicos basados en el tipo de acción solicitada.
    """
    if action == 'edit' and recipe.author != user and not user.is_staff:
        raise PermissionDenied("No tienes permiso para editar esta receta.")
    elif action == 'approve' and not user.is_staff:
        raise PermissionDenied("Solo los administradores pueden aprobar recetas.")
    elif action == 'delete' and recipe.author != user and not user.is_staff:
        raise PermissionDenied("No tienes permiso para eliminar esta receta.")
    return True
