from django import template

register = template.Library()


@register.filter
def check_high_health_permissions(user):
    allowed_groups = ["High Health", "Site Admin"]
    if user.groups.filter(name__in=allowed_groups).exists():
        return True
    elif user.profile.job_title.role.permission_groups.filter(
        name__in=allowed_groups
    ).exists():
        return True
    else:
        return False


register.filter("check_high_health_permissions", check_high_health_permissions)

