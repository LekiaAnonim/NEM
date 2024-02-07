from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from cloudinary.models import CloudinaryField
class HomePage(Page):
    template = 'home/home_page.html'
    # max_count = 1
    hero_section_message = RichTextField(blank=True)
    our_mission = RichTextField(blank=True)
    our_vision = RichTextField(blank=True)
    our_promise = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('hero_section_message'),
        FieldPanel('our_mission'),
        FieldPanel('our_vision'),
        FieldPanel('our_promise'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)
        testimonials = Testimonial.objects.all()
        faqs = FAQs.objects.all()
        
        context["testimonials"] = testimonials
        context["faqs"] = faqs
        return context

@register_snippet
class Testimonial(models.Model):
    full_name = models.CharField(max_length=500, null=True)
    message = RichTextField(blank=True)
    avatar = CloudinaryField("image", null=True)


    panels = [
        FieldPanel('full_name'),
        FieldPanel('message'),
        FieldPanel('avatar'),
    ]
    def __str__(self):
        return self.full_name
@register_snippet
class Faq(models.Model):
    question = models.CharField(max_length=500, null=True)
    answer = RichTextField(blank=True)

    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]
    def __str__(self):
        return self.question