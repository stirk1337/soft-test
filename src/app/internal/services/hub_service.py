from typing import List, Any

from app.internal.models.hub import Hub


def get_hubs() -> List[Hub]:
    return Hub.objects.filter()


def get_hub_by_parameter(parameter: str, value: Any) -> Hub | None:
    return Hub.objects.filter(**{parameter: value}).first()
