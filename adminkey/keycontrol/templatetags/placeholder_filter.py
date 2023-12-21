from django import template

register = template.Library()

@register.filter(name='placeholder')
def placeholder(field, placeholder_text):
    field.field.widget = field.field.widget.__class__(
        attrs={'placeholder': placeholder_text, 'class' : 'search'}
    )
    return field