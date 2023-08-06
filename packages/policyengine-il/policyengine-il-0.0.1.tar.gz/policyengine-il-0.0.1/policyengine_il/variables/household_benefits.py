from policyengine_il.model_api import *


class household_benefits(Variable):
    label = "benefits"
    entity = Household
    definition_period = YEAR
    value_type = float
    unit = "currency-ILS"
