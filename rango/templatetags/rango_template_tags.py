from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/all_categories.html')

def get_category_list(all_cat=None):
    return {'all_categories': Category.objects.all(),
            'active_all_cat': all_cat}
