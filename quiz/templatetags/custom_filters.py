from django import template
register = template.Library()

@register.filter
def subtract(value, arg):
    'return total question - correct question '
    return value - arg

from django import template

register = template.Library()

@register.filter
def get_selected(answers, question):
    return answers.filter(question=question).first().selected_choice if answers else None
