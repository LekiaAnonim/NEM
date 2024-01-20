from django import template
from waitlist.models import WaitlistFormSettings

register = template.Library()
# https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/


@register.simple_tag(takes_context=True)
def get_waitlist_form(context):
    request = context['request']
    waitlist_form_settings = WaitlistFormSettings.for_request(request)
    waitlist_form_page = waitlist_form_settings.waitlist_form_page.specific
    form = waitlist_form_page.get_form(
        page=waitlist_form_page, user=request.user)
    return {'page': waitlist_form_page, 'form': form}