from django import template

register = template.Library()


@register.filter
def check_high_health_permissions(user):
    allowed_groups = ["High Health", "Site Admin"]
    return (
        user.groups.filter(name__in=allowed_groups).exists()
        or user.profile.job_title.role.permission_group.filter(
            name__in=allowed_groups
        ).exists()
    )


register.filter("check_high_health_permissions", check_high_health_permissions)

