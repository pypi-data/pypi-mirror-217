from django import forms
from intecomm_form_validators.subject.health_economics import (
    HealthEconomicsHouseholdHeadFormValidator,
)

from ...models import HealthEconomicsHouseholdHead
from ..mixins import CrfModelFormMixin

# TODO: Remove NHIF and CHF from insurance Q for uganda


class HealthEconomicsHouseholdHeadForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HealthEconomicsHouseholdHeadFormValidator

    class Meta:
        model = HealthEconomicsHouseholdHead
        fields = "__all__"
