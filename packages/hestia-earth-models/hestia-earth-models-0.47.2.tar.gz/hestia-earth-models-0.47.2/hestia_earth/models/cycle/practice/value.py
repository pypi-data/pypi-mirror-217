"""
Practice Value

This model uses the lookup called "defaultValue" on each Practice to gap-fill a default value.
Otherwise, it calculates the `value` of the [Practice](https://hestia.earth/schema/Practice)
by taking an average from the `min` and `max` values.
"""
from hestia_earth.utils.tools import non_empty_list, list_average

from hestia_earth.models.utils.term import get_lookup_value

REQUIREMENTS = {
    "Cycle": {
        "practices": [{"@type": "Practice", "min": "", "max": ""}]
    }
}
RETURNS = {
    "Practice": [{
        "value": ""
    }]
}
MODEL_KEY = 'value'
LOOKUPS_KEY = 'defaultValue'


def _run(practice: dict):
    value = get_lookup_value(practice.get('term'), LOOKUPS_KEY) or list_average(
        practice.get('min') + practice.get('max')
    )
    return {**practice, MODEL_KEY: [value]}


def _should_run(practice: dict):
    should_run = all([
        len(practice.get(MODEL_KEY, [])) == 0,
        get_lookup_value(practice.get('term'), LOOKUPS_KEY) or all([
            len(practice.get('min', [])) > 0,
            len(practice.get('max', [])) > 0
        ])
    ])
    return should_run


def run(cycle: dict):
    practices = list(filter(_should_run, cycle.get('practices', [])))
    return non_empty_list(map(_run, practices))
