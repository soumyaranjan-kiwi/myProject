import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
        An abstract base class model that provides self-updating 'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class UuidTimeStampedModel(TimeStampedModel):
    """
        An abstract base class model that provides a UUID primary key field in addition to the TimeStampedModel fields.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(models.Model):
    """
        A model representing a user with a unique email address.
    """
    email = models.EmailField(unique=True)


class UserFile(UuidTimeStampedModel):
    """
        A model representing a user file with associated features and validations.
    """
    class EpicStatus(models.IntegerChoices):
        NON_REVIEWED = 1, _("Non-reviewed")
        REVIEWED = 2, _("Reviewed")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_files')
    epic = models.CharField(max_length=100)
    error_msg = models.TextField()
    start_date = models.DateField(null=True)
    status = models.SmallIntegerField(
        choices=EpicStatus.choices,
        default=EpicStatus.NON_REVIEWED,
        help_text='Used for epic status'
    )


class Feature(models.Model):
    """
        A model representing a feature associated with a user file.
    """
    user_file = models.ForeignKey(UserFile, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)


class FeatureValidation(models.Model):
    """
        A model representing a validation associated with a feature.
    """
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='validations')
    msg = models.TextField()
