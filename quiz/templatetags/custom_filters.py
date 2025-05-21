from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    try:
        return int(value) - int(arg)
    except Exception:
        return ''

@register.filter
def get_selected(answers, question):
    # Defensive: if no answers or no matching answer, return None
    if not answers:
        return None
    answer = answers.filter(question=question).first()
    if answer:
        return answer.selected_choice
    return None
