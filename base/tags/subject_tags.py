from django import template
from base.models import Subject

register = template.Library()


@register.simple_tag(name='get_subjects_html')
def get_subjects(name_filter=None, is_tech_filter=None):
    if not name_filter and not is_tech_filter:
        return Subject.objects.all()
    elif name_filter and not is_tech_filter:
        return Subject.objects.filter(name=name_filter)
    elif not name_filter and is_tech_filter:
        return Subject.objects.filter(is_tech=is_tech_filter)
    else:
        return Subject.objects.filter(name=name_filter, is_tech=is_tech_filter)

# OR

@register.inclusion_tag('base/subjects_tag.html', name='get_subjectsss_html')
def get_subjectsss(name_filter=None, is_tech_filter=None):
    if not name_filter and not is_tech_filter:
        subjects = Subject.objects.all()
    elif name_filter and not is_tech_filter:
        subjects = Subject.objects.filter(name=name_filter)
    elif not name_filter and is_tech_filter:
        subjects = Subject.objects.filter(is_tech=is_tech_filter)
    else:
        subjects = Subject.objects.filter(name=name_filter, is_tech=is_tech_filter)

    return {"sub_context": subjects}