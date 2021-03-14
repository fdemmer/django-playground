from django.db import models
from django.utils.translation import gettext_lazy as _


class CreatedDateMixin(models.Model):
    """
    Mixin adding created timestamp.
    """
    class Meta:
        abstract = True

    #: datetime when the object was created
    created_date = models.DateTimeField(
        _('Created date'),
        auto_now_add=True,
        editable=False,
    )


class DateFieldsMixin(CreatedDateMixin):
    """
    Mixin adding created and updated timestamps, as well as an order field.
    """
    class Meta:
        abstract = True
        ordering = ('-order', '-created_date',)

    #: datetime when the object was last modified
    updated_date = models.DateTimeField(
        _('Updated date'),
        auto_now=True,
        editable=False,
        db_index=True,
    )

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', None)
        if update_fields:
            kwargs['update_fields'] = set(update_fields).union({'updated_date'})
        super().save(*args, **kwargs)


class BaseModel(DateFieldsMixin, models.Model):
    class Meta:
        abstract = True


class Article(BaseModel):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
