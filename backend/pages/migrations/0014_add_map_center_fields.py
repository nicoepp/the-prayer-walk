# Generated by Django 3.1.13 on 2021-09-03 01:40

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_homepage_logotype'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField([('title', wagtail.core.blocks.CharBlock(form_classname='title', required=False)), ('paragraph', wagtail.core.blocks.TextBlock(form_classname='full')), ('rich', wagtail.core.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'ul', 'ol', 'bold', 'italic', 'link', 'document-link', 'hr'], form_classname='full'))]),
        ),
        migrations.AlterField(
            model_name='subpage',
            name='body',
            field=wagtail.core.fields.StreamField([('title', wagtail.core.blocks.CharBlock(form_classname='title', icon='title')), ('paragraph', wagtail.core.blocks.TextBlock(form_classname='full')), ('rich', wagtail.core.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'ul', 'ol', 'bold', 'italic', 'link', 'document-link', 'hr'], form_classname='full')), ('images', wagtail.core.blocks.StreamBlock([('image', wagtail.images.blocks.ImageChooserBlock())], icon='image')), ('video', wagtail.embeds.blocks.EmbedBlock(help_text='Paste in link to the video to be embedded at this spot. For example: https://vimeo.com/517009861'))]),
        ),
    ]