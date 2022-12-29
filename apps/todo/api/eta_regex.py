import re
from datetime import timedelta
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


def parse_new_eta_regex(command):
    project_issue_match = re.findall(create_eta_pattern, command)
    interval_matches = re.findall(create_eta_time_pattern, command)
    if not project_issue_match or not interval_matches:
        raise ValueError("Command is not valid.")

    project_name, issue_name = project_issue_match[0]

    # TODO: implement expected_date creation
    # eta_verbose_end, eta_date_end, eta_time_end = interval_matches[0]
    # expected_at_date = None

    return project_name, issue_name, timezone.now()


def create_new_eta(command: str, user) -> Expectation:
    project_name, issue_name, expected_at_date = parse_new_eta_regex(command)

    if Expectation.objects.filter(project__name=project_name, issue=issue_name, user=user).exists():
        raise ValueError("Duplicate project or issue")

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
