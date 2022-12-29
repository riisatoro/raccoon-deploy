from enum import Enum

from apps.todo.models import Expectation


class IntervalTypeEnum(Enum):
    m = "minutes"
    h = "hours"
    d = "days"


def parse_new_eta_regex(command):
    ...


def create_new_eta(command: str) -> Expectation:
    ...


def extends_existed_eta(command: str, eta: Expectation) -> Expectation:
    ...
