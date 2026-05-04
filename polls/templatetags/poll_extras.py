from django import template
from polls.models import Categories, Questions

register = template.Library()

@register.simple_tag()
def tag_categories():
    return Categories.objects.all()

@register.simple_tag()
def tag_questions(category_slug=None):
    if category_slug and category_slug != 'all':
        return Questions.objects.filter(category__slug=category_slug)
    return Questions.objects.all()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    for kwarg, value in kwargs.items():
        query[kwarg] = value
    
    return query.urlencode()

@register.inclusion_tag('polls/includes/wizard_modal.html', takes_context=True)
def render_wizard(context):
    request = context['request']
    user = request.user
    
    wizard_question = None
    
    if request.GET.get('wizard') == '1':

        if request.GET.get('refresh') == '1':
            request.session['wizard_viewed'] = []
        
        viewed_ids = request.session.get('wizard_viewed', [])
        
        exclude_ids = set(viewed_ids)
        
        if user.is_authenticated:
            voted_ids = user.polls_voted.values_list("id", flat=True)
            exclude_ids.update(voted_ids)
        
        wizard_question = Questions.objects.exclude(id__in=exclude_ids).order_by('?').first()
        
        if wizard_question:
            viewed_ids.append(wizard_question.id)
            request.session['wizard_viewed'] = viewed_ids
            
    return {
        'wizard_question': wizard_question,
        'request': request,
    }