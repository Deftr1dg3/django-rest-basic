from django.db import models
# Allowing Generic relationships
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import QuerySet

# Create your models here.

# Custom manager
class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type: models.Model, obj_id: int) -> QuerySet:
        content_type = ContentType.objects.get_for_model(obj_type)
        queryset = TaggedItem.objects \
            .select_related('tag') \
            .filter(
            content_type=content_type,
            object_id=obj_id
        )
        return queryset


class Tag(models.Model):
    label = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.label}'
    

class TaggedItem(models.Model):
    # Add manager
    # Overriding attribute 'objects' to get custom manager class on its call.
    objects = TaggedItemManager()
    #  What tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # To identify object without explicitly import it.
    # 1. Type (product, video, article) of the object
    # 2. ID
    # Using django.contrib.contenttypes from INSTALLED_APPS, we can create Generic
    # relationshipt within our models
    # To define generic relationship we need to define next three fields:
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # This solution can work only if the PK of the object is Integer.
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    