from django.core.validators import MinValueValidator
from django.db import models


class Hub(models.Model):
    url = models.URLField(max_length=500, unique=True)
    parse_period = models.IntegerField(validators=[MinValueValidator(0)])
