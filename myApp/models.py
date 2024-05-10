import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class UuidTimeStampedModel(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(models.Model):
    email = models.EmailField(unique=True)


class UserFile(UuidTimeStampedModel):
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
    user_file = models.ForeignKey(UserFile, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)


class FeatureValidation(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='validations')
    msg = models.TextField()
