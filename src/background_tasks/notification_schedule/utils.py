from dateutil.relativedelta import relativedelta

from notification_schedule.constants import RepeatInterval


FACTORY_RELATIVE_PARAMS = {
    RepeatInterval.DAILY.value: lambda step: {"days": step},
    RepeatInterval.WEEKLY.value: lambda step: {"weeks": step},
    RepeatInterval.MONTHLY.value: lambda step: {"months": step},
    RepeatInterval.YEARLY.value: lambda step: {"years": step},
}

def factory_relativedelta(interval: str, step: int) -> relativedelta:
    # FACTORY_RELATIVE_PARAMS[interval] returns an anonymous function
    # the  anonymous function takes "step" as param, and it returns a dict
    delta = FACTORY_RELATIVE_PARAMS[interval](step)
    return relativedelta(**delta)
