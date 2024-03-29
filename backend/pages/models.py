from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel

from backend.streetsignup.models import City


Page.show_in_menus_default = True

RICHTEXT_FEATURES = ['h2', 'h3', 'h4', 'ul', 'ol', 'bold', 'italic', 'link', 'document-link', 'hr']


class HomePage(Page):
    event_date = models.CharField(blank=True, default='', max_length=50)
    logotype = models.ForeignKey(Image,         null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    background_image = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    body = StreamField([
        ('title', blocks.CharBlock(form_classname='title', required=False)),
        ('paragraph', blocks.TextBlock(form_classname='full')),
        ('rich', blocks.RichTextBlock(form_classname='full', features=RICHTEXT_FEATURES)),
    ])
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    attribution = models.CharField(blank=True, default='', max_length=120)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    city = models.ForeignKey(City, related_name='homepage', on_delete=models.PROTECT)

    content_panels = Page.content_panels + [
        FieldPanel('event_date'),
        ImageChooserPanel('logotype'),
        ImageChooserPanel('background_image'),
        StreamFieldPanel('body'),
        MultiFieldPanel(
            [
                FieldPanel('facebook'),
                FieldPanel('instagram'),
                FieldPanel('attribution'),
            ],
            heading='Footer',
            classname='collapsible',
        ),
    ]
    settings_panels = Page.settings_panels + [
        FieldPanel('city'),
        FieldRowPanel(
            [
                FieldPanel('latitude'),
                FieldPanel('longitude'),
            ],
            heading='Map Center',
        ),
    ]

    parent_page_types = [Page]

    def get_context(self, request, *args, **kwargs):
        ctx = super().get_context(request, *args, **kwargs)

        streets = self.city.street_set
        ctx['streets_covered'] = streets.annotate(subs=models.Count('subscriptions')).filter(subs__gt=0).count()
        ctx['streets_total'] = streets.count()
        return ctx


class MenuPage(Page):
    icon = models.CharField('Menu Icon', default='fa-info-circle', max_length=30)

    def get_context(self, request, *args, **kwargs):
        ctx = super().get_context(request, *args, **kwargs)

        ctx['site_root'] = self.get_site().root_page.specific

        return ctx

    class Meta:
        abstract = True


class SubPage(MenuPage):
    body = StreamField([
        ('title', blocks.CharBlock(form_classname='title', icon='title')),
        ('paragraph', blocks.TextBlock(form_classname='full')),
        ('rich', blocks.RichTextBlock(form_classname='full', features=RICHTEXT_FEATURES)),
        ('images', blocks.StreamBlock([('image', ImageChooserBlock())], icon='image')),
        ('video', EmbedBlock(help_text='Paste in link to the video to be embedded at this spot. '
                                       'For example: https://vimeo.com/517009861')),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('icon'),
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['pages.HomePage']
    subpage_types = []


class SignUpPage(MenuPage):
    content_panels = Page.content_panels + [
        FieldPanel('icon'),
    ]

    parent_page_types = ['pages.HomePage']
    subpage_types = []
    max_count_per_parent = 1


class MapPage(MenuPage):
    content_panels = Page.content_panels + [
        FieldPanel('icon'),
    ]

    parent_page_types = ['pages.HomePage']
    subpage_types = []
    max_count_per_parent = 1
