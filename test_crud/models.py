from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

# Create your models here.


class logs(models.Model):
    has_mutation = models.BooleanField(default=False, verbose_name=_("¿Tiene mutación?"))
    success = models.BooleanField(default=False, verbose_name=_("¿Finalizo correctamente?"))
    dna_provided = models.CharField(max_length=1000,blank=True, null=True, verbose_name=_("Cadena de ADN proporcionada"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))

    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")