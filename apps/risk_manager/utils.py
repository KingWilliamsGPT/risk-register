from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string


def get_app_permissions(app_name):
    """
    Returns all permissions for a given app name.

    Args:
    app_name (str): The name of the Django app.

    Returns:
    list: A list of tuples containing (codename, name) for each permission.
    """
    try:
        app_config = apps.get_app_config(app_name)
    except LookupError:
        return []  # Return an empty list if the app doesn't exist

    permissions = []
    for model in app_config.get_models():
        content_type = ContentType.objects.get_for_model(model)
        perms = Permission.objects.filter(content_type=content_type)
        permissions.extend([(p.codename, p.name) for p in perms])

    return permissions

# Example usage:
# all_permissions = get_app_permissions('your_app_name')
# for codename, name in all_permissions:
#     print(f"Codename: {codename}, Name: {name}")


def get_app_perms(*app_names):
    permissions = []
    for app_name in app_names:
        permissions.extend([f'{app_name}:{perm}' for perm, _ in get_app_permissions(app_name)])
    return permissions


def render_template(template_name, context):
    """
    Renders a template with the provided context and returns it as a string.

    Args:
        template_name (str): The path to the template to render.
        context (dict): The context dictionary to pass to the template.

    Returns:
        str: The rendered template as a string.
    """
    return render_to_string(template_name, context)
