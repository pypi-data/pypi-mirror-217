from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import DeathReportTmgModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import intecomm_ae_admin
from ..forms import DeathReportTmgSecondForm
from ..models import DeathReportTmgSecond


@admin.register(DeathReportTmgSecond, site=intecomm_ae_admin)
class DeathReportTmgSecondAdmin(DeathReportTmgModelAdminMixin, SimpleHistoryAdmin):
    form = DeathReportTmgSecondForm
