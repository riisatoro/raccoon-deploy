import re
from datetime import datetime, timedelta
from enum import Enum

from django.utils import timezone

from apps.todo.models import Expectation, Project

create_eta_pattern = r"(\w+)#(\w+)\W+"
create_eta_time_pattern = r"\w+#\w+\sat\s(tomorrow)?\s?(\d{2}-\d{2})?\s?(\d{2}:\d{2})"
extends_eta_pattern = r"eta\s\+(\d+)([m|d|h])"


class IntervalTypeEnum(Enum):
    m = "minutes"
    h = "hours"
    d = "days"


def create_eta_time(date: datetime, time: str) -> datetime:
    hours, minutes = time.split(":")
    return date.replace(hour=int(hours), minute=int(minutes))


def create_eta_date(verbose: str, date: str) -> datetime:
    expected_at = timezone.now()

    if date:
        month, day = date.split("-")
        expected_at += timedelta(day=int(day), month=int(month))
    elif verbose == "tommorow":
        expected_at += timedelta(days=1)

    return expected_at


def parse_command_info(command: str) -> list[tuple[str]]:
    project_issue_match = re.findall(create_eta_pattern, command)
    interval_match = re.findall(create_eta_time_pattern, command)
    if not project_issue_match:
        raise ValueError("Can't parse the project & issue info.")
    if not interval_match:
        raise ValueError("Can't parse the project & issue time interval.")

    return project_issue_match[0], interval_match[0]


def parse_new_eta_regex(command: str) -> list[str | datetime]:
    project_data, date_data = parse_command_info(command)

    project_name, issue_name = project_data
    eta_verbose_end, eta_date_end, eta_time_end = date_data

    expected_at = create_eta_date(eta_verbose_end, eta_date_end)
    expected_at = create_eta_time(expected_at, eta_time_end)

    return project_name, issue_name, expected_at


def create_new_eta(command: str, user) -> Expectation:
    project_name, issue_name, expected_at_date = parse_new_eta_regex(command)

    project, _ = Project.objects.get_or_create(name=project_name)
    expectation = Expectation.objects.create(
        project=project,
        user=user,
        issue=issue_name,
        expected_at=expected_at_date,
    )
    return expectation


def extends_existed_eta(command: str, eta: Expectation) -> Expectation:
    if command == "eta done":
        eta.done_at = timezone.now()
        eta.save()
        return eta

    matches = re.findall(extends_eta_pattern, command)
    if not matches or len(matches[0]) != 2:
        raise ValueError("Command is not valid.")

    value, interval_type = matches[0]
    payload = {IntervalTypeEnum[interval_type].value: int(value)}

    eta.expected_at += timedelta(**payload)
    eta.save()
    return eta
