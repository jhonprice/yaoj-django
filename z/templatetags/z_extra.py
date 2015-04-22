from django.template import Library
from django.template.defaultfilters import stringfilter
from markdown import markdown as md


register = Library()


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    return md(value, ['markdown.extensions.codehilite'],
              output_format='HTML5')
